/*
A KBase module: kb_sourmash
*/

module kb_sourmash {
    /*
        Insert your typespec information here.
    */

    /*
        An X/Y/Z style workspace object reference
    */
    typedef string obj_upa;

    typedef structure {
        string input_assembly_upa;
        string workspace_name;
        string search_db;
        int scaled;
    } SourmashParams;

    typedef structure {
        string report_name;
        string report_ref;
    } SourmashResults;

    funcdef run_sourmash(SourmashParams params)
        returns(SourmashResults results) authentication required;

    typedef structure {
        list<obj_upa> object_list;
        string workspace_name;
        int scaled;
    } SourmashCompareParams;

    funcdef run_sourmash_compare(SourmashCompareParams)
        returns(SourmashResults results) authentication required;
};
