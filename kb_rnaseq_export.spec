/*
A KBase module: kb_rnaseq_export
*/

module kb_rnaseq_export {
    typedef structure {
        string input_ref;
        string destination_dir;
    } ExportStagingParams;
    typedef structure {
        string path;
    } ExportStagingOutput;
    funcdef export_rna_seq_alignment_as_bam_to_staging (ExportStagingParams params) returns (ExportStagingOutput output) authentication required;


};
