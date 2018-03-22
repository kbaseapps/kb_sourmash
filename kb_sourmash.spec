/*
A KBase module: kb_sourmash
*/

module kb_sourmash {
    /*
        Insert your typespec information here.
    */


    typedef structure {
        string input_assembly_upa;
        string workspace_name;
    } SourmashParams;

    typedef structure {
        string report_name;
        string report_ref;
    } SourmashResults;

    funcdef run_sourmash(SourmashParams)
        returns(SourmashResults) authentication required;
};
