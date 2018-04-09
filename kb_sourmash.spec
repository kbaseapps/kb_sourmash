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

    /*
    A boolean - 0 for false, 1 for true.
        @range (0, 1)
    */
    typedef int boolean;

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

    funcdef run_sourmash_compare(SourmashCompareParams params)
        returns(SourmashResults results) authentication required;

    typedef structure {
        obj_upa input_assembly_upa;
        string workspace_name;
        string search_db;
        int scaled;
        boolean containment;
    } SourmashSearchParams;

    funcdef run_sourmash_search(SourmashSearchParams params)
        returns (SourmashResults results) authentication required;

    typedef structure {
        obj_upa input_assembly_upa;
        string workspace_name;
        string search_db;
        int scaled;
    } SourmashGatherParams;

    funcdef run_sourmash_gather(SourmashGatherParams params)
        returns (SourmashResults results) authentication required;
};
