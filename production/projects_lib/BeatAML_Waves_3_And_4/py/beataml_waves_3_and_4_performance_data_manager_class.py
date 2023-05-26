# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
from nlp_pipeline_lib.manager_lib.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager
from projects_lib.BeatAML_Waves_3_And_4.py.beataml_waves_3_and_4_specimens_manager_class \
    import BeatAML_Waves_3_And_4_specimens_manager as Specimens_manager
from tools_lib.processing_tools_lib.function_processing_tools \
    import parallel_composition, sequential_composition
    
#
def _get_nlp_value(arg_dict):
    identifier = arg_dict['identifier']
    nlp_values = arg_dict['nlp_values']
    validation_datum_key = arg_dict['validation_datum_key']
    if identifier in nlp_values.keys():
        keys0 = list(nlp_values[identifier])
        if validation_datum_key in nlp_values[identifier][keys0[0]].keys():
            nlp_value = nlp_values[identifier][keys0[0]][validation_datum_key]
        else:
            nlp_value = None
    else:
        nlp_value = None
    return nlp_value
    
#
class BeatAML_Waves_3_And_4_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_object, evaluation_manager,
                 json_manager_registry, metadata_manager,
                 xls_manager_registry):
        Performance_data_manager.__init__(self, static_data_object,
                                          evaluation_manager,
                                          json_manager_registry,
                                          metadata_manager,
                                          xls_manager_registry)
        static_data = self.static_data_object.get_static_data()
        if static_data['project_subdir'] == 'test':
            self.identifier_key = 'MRN'
            self.identifier_list = static_data['patient_list']
            self.queries = static_data['queries_list']
    
    #
    def _get_nlp_data(self, data_in, queries):
        data_out = {}
        for query in queries:
            key = query[0]
            sections = query[1]
            query_name = query[2]
            data_key = query[3]
            mode_flg = query[4]
            strip_flg = query[5]
            data_out[key] = \
                self._get_data_value(data_in, sections,
                                     query_name + '_' + self.nlp_value_key,
                                     data_key, mode_flg=mode_flg)
            if strip_flg and data_out[key] is not None:
                data_out[key] = data_out[key][0]
        del_keys = []
        for key in data_out:
            if data_out[key] is None:
                del_keys.append(key)
        for key in del_keys:
            del data_out[key]  
        if not data_out:
            data_out = None
        return data_out
    
    #
    def _get_nlp_values(self, nlp_data, data_json):
        metadata_keys, metadata_dict_dict = self._read_metadata(nlp_data)
        specimens_manager = Specimens_manager(self.static_data_object,
                                              metadata_dict_dict)
        specimens_manager.generate_document_map(data_json, 'file_map.txt')
        specimens_manager.generate_json_file(self.directory_manager.pull_directory('log_dir'), 'validation.json')
        nlp_values = specimens_manager.get_data_json()
        return nlp_values
    
    #
    def _get_validation_idx(self, validation_data_manager, validation_datum_key):
        column_labels = validation_data_manager.column_labels()
        validation_idx_list = \
            [k for k in range(len(column_labels)) \
             if column_labels[k] == validation_datum_key]
        if len(validation_idx_list) > 0:
            validation_idx = validation_idx_list[0]
        else:
            validation_idx = None
        return validation_idx
    
    #
    def _get_validation_value(self, arg_dict):
        identifier = arg_dict['identifier']
        validation_datum_key = arg_dict['validation_datum_key']
        validation_value = None
        for j in range(1, self.validation_data_manager.length()):
            row = self.validation_data_manager.row(j)
            if row[0] == identifier:
                validation_value = \
                    self._process_validation_item(j, validation_datum_key)
        return validation_value
            
    #
    def _process_performance(self, nlp_values_in, validation_datum_keys,
                             display_flg):
        self._initialize_performance_dicts()
        nlp_values = \
            self._identify_manual_review(nlp_values_in, validation_datum_keys)
        validation_datum_keys = []
        for query in self.queries:
            validation_datum_keys.append(query[0])
        labId_list = None
        patientIds = list(set(nlp_values.keys()))
        N_documents = 0
        for patientId in patientIds:
            if patientId in nlp_values_in:
                nlp_values = nlp_values_in[patientId]
            else:
                nlp_values = []
            labIds = []
            labIds.extend(nlp_values.keys())
            for labId in labIds:
                print(labId)
                N_documents += 1
                for i in range(len(self.queries)):
                    validation_datum_key = self.queries[i][0]
                    arg_dict = {}
                    arg_dict['identifier'] = labId
                    arg_dict['nlp_values'] = nlp_values
                    arg_dict['validation_datum_key'] = validation_datum_key
                    return_dict = parallel_composition([self._get_validation_value,
                                                        _get_nlp_value], arg_dict)
                    arg_dict = {}
                    arg_dict['display_flg'] = display_flg
                    arg_dict['identifier'] = labId
                    arg_dict['identifier_list'] = labId_list
                    arg_dict['nlp_value'] = \
                        return_dict[_get_nlp_value.__name__]
                    arg_dict['validation_datum_key'] = validation_datum_key
                    arg_dict['validation_value'] = \
                        return_dict[self._get_validation_value.__name__]
                    sequential_composition([self.evaluation_manager.evaluation,
                                            self._update_performance_dicts],
                                           arg_dict)
                    nlp_value = return_dict[_get_nlp_value.__name__]
                    self._append_csv_header(validation_datum_key + ', ')
                    self._append_csv_body(nlp_value, newline_flg=False)
        self._evaluate_performance(N_documents)
        
    #
    def _process_validation_item(self, row_idx, validation_datum_key):
        row = self.validation_data_manager.row(row_idx)
        validation_idx = \
            self._get_validation_idx(self.validation_data_manager,
                                     validation_datum_key)
        if validation_idx is not None:
            x = row[validation_idx]
            if x == '':
                x = None
        else:
            x = None
        return x
    
    #
    def _read_metadata(self, nlp_data):
        metadata_keys = []
        metadata_dict_dict = {}
        for key in nlp_data.keys():
            metadata_dict_dict[key] = {}
            metadata_dict_dict[key]['METADATA'] = \
                nlp_data[key]['METADATA']
            metadata_dict_dict[key]['NLP_METADATA'] = \
                nlp_data[key]['NLP_METADATA']
        for metadata_key in metadata_dict_dict.keys():
            for key in metadata_dict_dict[metadata_key].keys():
                if key not in metadata_keys:
                    metadata_keys.append(key)
        return metadata_keys, metadata_dict_dict
            
    #
    def _read_nlp_value(self, nlp_data, data_json, key, identifier):
        doc_name = str(key)
        preprocessed_text = nlp_data[key][self.nlp_source_text_key]
        if 'PROC_NM' in nlp_data[key][self.metadata_key].keys():
            proc_nm = nlp_data[key][self.metadata_key]['PROC_NM']
        else:
            proc_nm = nlp_data[key][self.metadata_key]['PROC_NAME']
        result_date = nlp_data[key][self.metadata_key]['RESULT_COMPLETED_DT']
        specimen_date = nlp_data[key][self.metadata_key]['SPECIMEN_COLL_DT']
        data_in = nlp_data[key][self.nlp_data_key]
        data_out = self._get_nlp_data(data_in, self.queries)
        if data_out is not None:
            for key in data_out:
                data_out[key] = [ data_out[key] ]
        if data_out is not None:
            doc_label = ''
            if 'bone marrow' in preprocessed_text.lower():
                doc_label += 'BLD'
            elif 'peripheral blood' in preprocessed_text.lower():
                doc_label += 'BLD'
            if 'CSF' in preprocessed_text:
                doc_label += 'CSF'
            if doc_label == '':
                doc_label = 'NA'
            if identifier not in data_json:
                data_json[identifier] = {}
            if specimen_date not in data_json[identifier]:
                data_json[identifier][specimen_date] = {}
            if proc_nm not in data_json[identifier][specimen_date]:
                data_json[identifier][specimen_date][proc_nm] = {}
            if doc_name not in data_json[identifier][specimen_date][proc_nm].keys():
                data_json[identifier][specimen_date][proc_nm][doc_name + '_' + doc_label + '_' + result_date] = data_out
        return data_json