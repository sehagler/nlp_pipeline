# Copyright 2021, Linguamatics Ltd.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import ntpath
import os
import posixpath
import sys
from argparse import ArgumentParser
from collections import defaultdict
from contextlib import contextmanager
from pathlib import Path

import rtyaml
import yaml


class QueryFixer(object):
    def __init__(self, query_file_path, query_folder, dry_run=False, logger=None):
        self.logger = logger or get_logger(logging.CRITICAL)
        self.query_file_path = query_file_path
        self.query_folder = query_folder
        self.dry_run = dry_run
        self.resolved_issues = []
        self.unresolved_issues = []

    def recurse_container(self, query_item):
        if isinstance(query_item, dict):
            for value in query_item.values():
                for sub_item in self.recurse_container(value):
                    yield sub_item
        elif isinstance(query_item, (list, set, tuple)):
            for element in query_item:
                for sub_item in self.recurse_container(element):
                    yield sub_item
        else:
            yield query_item

    def query_reference_iter(self, query):
        """
        Find all references to subqueries or embedded queries within a parsed query
        Args:
            query: parsed query

        Yields:
            str: reference to subquery or embedded query
        """
        for query_item in self.recurse_container(query):
            if isinstance(query_item, str) and query_item.endswith(".i2qy"):
                yield query_item

    def check_query_references(self, query, query_folder):
        """
        Check that a query's references are relative and not broken

        Args:
            query: parsed query
            query_folder (Path): query folder for checking relative paths

        Yields:
            str: any warnings about the query reference
        """
        for query_ref in self.query_reference_iter(query):
            issue = None
            if posixpath.isabs(query_ref) or ntpath.isabs(query_ref):
                if query_ref.startswith("/api;type=saved_query"):
                    issue = "Contains absolute URL reference {}".format(query_ref)
                elif os.path.isfile(query_ref):
                    issue = "Contains absolute path {}".format(query_ref)
                else:
                    issue = "Contains broken absolute path {}".format(query_ref)
            else:
                referenced_query_path = query_folder / query_ref
                if not referenced_query_path.is_file():
                    issue = "Contains broken relative path {}".format(query_ref)
            if issue:
                self.unresolved_issues.append(issue)

    def remove_snapshots(self, query):
        if "querySnapshots" in query:
            query.pop("querySnapshots")
            self.resolved_issues.append("Containing query snapshots")

    def check_query(self, query_file_path):
        with query_file_path.open(encoding="utf8") as query_file:
            try:
                query = rtyaml.load(query_file)
            except Exception:
                #traceback.print_exc()
                query_file.seek(0)
                contents = query_file.read()
                if contents.strip():
                    issue = "Invalid query: could not parse YAML"
                else:
                    issue = "Invalid query: file is empty"
                self.unresolved_issues.append(issue)
                return [], self.unresolved_issues

        self.check_query_references(query, query_file_path.parent)

        self.remove_snapshots(query)

        if self.dry_run:
            return [], self.resolved_issues + self.unresolved_issues
        else:
            if self.resolved_issues:
                with query_file_path.open(mode="w", encoding="utf8") as query_file:
                    rtyaml.dump(query, query_file)
            return self.resolved_issues, self.unresolved_issues


class QuerySetFixer(object):
    def __init__(self, *query_paths, **kwargs):
        self.logger = kwargs.get("logger") or get_logger(logging.CRITICAL)
        self.dry_run = kwargs.get("dry_run") or False
        self.query_paths = query_paths

    def query_file_path_iter(self):
        for query_path in self.query_paths:
            query_path = Path(query_path)
            if query_path.is_dir():
                for query_file_path in query_path.rglob("*.i2qy"):
                    if query_file_path.is_file():
                        yield query_file_path, query_path
            elif query_path.is_file() and query_path.match("*.i2qy"):
                yield query_path, None

    def sort_queries(self):
        """
        Check queries and sort them by whether they pass the checks,
        so that the queries with warnings that require attention are
        reported last, to avoid having to scroll up to find them.

        Returns:
            dict: query paths with their issues, keyed by status
        """
        logger = self.logger
        # (resolved,unresolved) -> (path, resolved_issues, unresolved_issues)
        sorted_queries = defaultdict(list)
        for query_file_path, query_folder in self.query_file_path_iter():
            logger.debug("Parsing query {}".format(query_file_path))
            query_fixer = QueryFixer(
                query_file_path, query_folder, dry_run=self.dry_run, logger=self.logger
            )
            query_results = query_fixer.check_query(query_file_path)
            resolved_issues, unresolved_issues = query_results
            has_resolved_issues = bool(resolved_issues)
            has_unresolved_issues = bool(unresolved_issues)
            query_status = (has_resolved_issues, has_unresolved_issues)
            query_report = (query_file_path, resolved_issues, unresolved_issues)
            sorted_queries[query_status].append(query_report)
        return sorted_queries

    def check_queries(self):
        logger = self.logger
        query_results = self.sort_queries()
        ok_queries = [query_path for query_path, _, _ in query_results[(False, False)]]
        resolved_queries = [
            (query_path, resolved_issues)
            for query_path, resolved_issues, _ in query_results[(True, False)]
        ]
        flagged_queries = query_results[(False, True)] + query_results[(True, True)]
        for query_path in ok_queries:
            logger.info("Query OK: {}".format(query_path))
        for query_path, resolved_issues in resolved_queries:
            logger.info("Query OK after resolving the issues: {}".format(query_path))
            for resolved_issue in resolved_issues:
                logger.info("\t- Resolved: {}".format(resolved_issue))
        for query_path, resolved_issues, unresolved_issues in flagged_queries:
            logger.warning("Query not OK: {}".format(query_path))
            for resolved_issue in resolved_issues:
                logger.info("\t- Resolved: {}".format(resolved_issue))
            for unresolved_issue in unresolved_issues:
                logger.warning("\t- Unresolved: {}".format(unresolved_issue))
        if flagged_queries:
            return False
        else:
            if resolved_queries:
                logger.info("All Queries OK (after some modifications)")
            else:
                logger.info("All Queries OK")
            return True


class InfoFilter(logging.Filter):
    """
    Filter for stream handler for stdout.
    Only logs INFO and DEBUG,
    since WARNING, ERROR and CRITICAL should go to stderr.
    """

    def filter(self, record):
        if record.levelno >= logging.WARNING:
            return False
        return super(InfoFilter, self).filter(record)


def get_logger(level=logging.WARNING, log_file_path=None):
    logger = logging.getLogger("i2e_query_check")
    logger.setLevel(level)
    formatter = logging.Formatter("%(message)s")
    if log_file_path:
        log_file_handler = logging.FileHandler(log_file_path, mode="w")
        log_file_handler.setFormatter(formatter)
        log_file_handler.setLevel(logging.DEBUG)
        logger.addHandler(log_file_handler)
        return logger
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.addFilter(InfoFilter())
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.DEBUG)
    logger.addHandler(stdout_handler)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(logging.WARNING)
    logger.addHandler(stderr_handler)
    return logger


def get_parser():
    desc = (
        "Remove snapshots from queries and "
        "check for absolute/broken paths for "
        "subqueries and embedded queries. "
        "Exits 1 if any issues are found with any queries, otherwise 0."
    )
    parser = ArgumentParser(description=desc)
    parser.add_argument(
        "query_paths", nargs="+", help="File/folder paths to queries to be checked."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help=(
            "Report issues with queries, "
            "but do not make any modifications (such as cleaning snapshots)."
        ),
    )
    parser.add_argument(
        "--log", default=None, help="Output to a file instead of the terminal"
    )
    mutually_exclusive_group = parser.add_mutually_exclusive_group()
    mutually_exclusive_group.add_argument(
        "--errors-only",
        action="store_true",
        default=False,
        help="Only display queries with issues.",
    )
    mutually_exclusive_group.add_argument(
        "--debug", action="store_true", default=False, help="Display low-level info"
    )
    return parser


def main(args=None):
    parser = get_parser()
    parsed_args = parser.parse_args(args=args)

    log_level = logging.INFO
    if parsed_args.debug:
        log_level = logging.DEBUG
    elif parsed_args.errors_only:
        log_level = logging.WARNING

    with yaml_constructor():
        query_fixer = QuerySetFixer(
            *parsed_args.query_paths,
            dry_run=parsed_args.dry_run,
            logger=get_logger(log_level, log_file_path=parsed_args.log)
        )
        all_queries_ok = query_fixer.check_queries()
    return 0 if all_queries_ok else 1


# Work around for https://github.com/yaml/pyyaml/issues/89
# which causes problems with solitary, unquoted '=' characters
def construct_value(load, node):
    """Add an ad hoc node to avoid ConstructorError in PyYaml

    Args:
        load (yaml.loader.SafeLoader): YAML loader
        node (yaml.nodes.ScalarNode): YAML scalar node

    Yields:
        str: Node value
    """
    if not isinstance(node, yaml.ScalarNode):
        raise yaml.constructor.ConstructorError(
            "while constructing a value",
            node.start_mark,
            "expected a scalar, but found %s" % node.id,
            node.start_mark,
        )
    yield str(node.value)


@contextmanager
def yaml_constructor():
    """
    Context manager for temporarily adding the YAML constructor,
    reverting it afterwards to its original value,
    to avoid overwriting anyone else's global state.
    """
    tag = u"tag:yaml.org,2002:value"
    remove_afterwards = tag not in rtyaml.Loader.yaml_constructors
    original_value = rtyaml.Loader.yaml_constructors.get(tag)
    rtyaml.Loader.add_constructor(tag, construct_value)
    yield None
    if remove_afterwards:
        rtyaml.Loader.yaml_constructors.pop(tag)
    else:
        rtyaml.Loader.yaml_constructors[tag] = original_value


if __name__ == "__main__":
    sys.exit(main())
