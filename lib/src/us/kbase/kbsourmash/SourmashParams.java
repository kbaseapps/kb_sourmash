
package us.kbase.kbsourmash;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: SourmashParams</p>
 * <pre>
 * Insert your typespec information here.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_assembly_upa",
    "workspace_name",
    "search_db"
})
public class SourmashParams {

    @JsonProperty("input_assembly_upa")
    private String inputAssemblyUpa;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("search_db")
    private String searchDb;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_assembly_upa")
    public String getInputAssemblyUpa() {
        return inputAssemblyUpa;
    }

    @JsonProperty("input_assembly_upa")
    public void setInputAssemblyUpa(String inputAssemblyUpa) {
        this.inputAssemblyUpa = inputAssemblyUpa;
    }

    public SourmashParams withInputAssemblyUpa(String inputAssemblyUpa) {
        this.inputAssemblyUpa = inputAssemblyUpa;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public SourmashParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("search_db")
    public String getSearchDb() {
        return searchDb;
    }

    @JsonProperty("search_db")
    public void setSearchDb(String searchDb) {
        this.searchDb = searchDb;
    }

    public SourmashParams withSearchDb(String searchDb) {
        this.searchDb = searchDb;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((("SourmashParams"+" [inputAssemblyUpa=")+ inputAssemblyUpa)+", workspaceName=")+ workspaceName)+", searchDb=")+ searchDb)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
