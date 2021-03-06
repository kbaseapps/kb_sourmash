
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
 * <p>Original spec-file type: SourmashSearchParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_assembly_upa",
    "workspace_name",
    "search_db",
    "scaled",
    "containment"
})
public class SourmashSearchParams {

    @JsonProperty("input_assembly_upa")
    private String inputAssemblyUpa;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("search_db")
    private String searchDb;
    @JsonProperty("scaled")
    private Long scaled;
    @JsonProperty("containment")
    private Long containment;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_assembly_upa")
    public String getInputAssemblyUpa() {
        return inputAssemblyUpa;
    }

    @JsonProperty("input_assembly_upa")
    public void setInputAssemblyUpa(String inputAssemblyUpa) {
        this.inputAssemblyUpa = inputAssemblyUpa;
    }

    public SourmashSearchParams withInputAssemblyUpa(String inputAssemblyUpa) {
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

    public SourmashSearchParams withWorkspaceName(String workspaceName) {
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

    public SourmashSearchParams withSearchDb(String searchDb) {
        this.searchDb = searchDb;
        return this;
    }

    @JsonProperty("scaled")
    public Long getScaled() {
        return scaled;
    }

    @JsonProperty("scaled")
    public void setScaled(Long scaled) {
        this.scaled = scaled;
    }

    public SourmashSearchParams withScaled(Long scaled) {
        this.scaled = scaled;
        return this;
    }

    @JsonProperty("containment")
    public Long getContainment() {
        return containment;
    }

    @JsonProperty("containment")
    public void setContainment(Long containment) {
        this.containment = containment;
    }

    public SourmashSearchParams withContainment(Long containment) {
        this.containment = containment;
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
        return ((((((((((((("SourmashSearchParams"+" [inputAssemblyUpa=")+ inputAssemblyUpa)+", workspaceName=")+ workspaceName)+", searchDb=")+ searchDb)+", scaled=")+ scaled)+", containment=")+ containment)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
