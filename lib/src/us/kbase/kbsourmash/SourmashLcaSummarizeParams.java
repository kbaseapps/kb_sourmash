
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
 * <p>Original spec-file type: SourmashLcaSummarizeParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_assembly_upa",
    "workspace_name",
    "lca_search_db",
    "scaled"
})
public class SourmashLcaSummarizeParams {

    @JsonProperty("input_assembly_upa")
    private String inputAssemblyUpa;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("lca_search_db")
    private String lcaSearchDb;
    @JsonProperty("scaled")
    private Long scaled;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_assembly_upa")
    public String getInputAssemblyUpa() {
        return inputAssemblyUpa;
    }

    @JsonProperty("input_assembly_upa")
    public void setInputAssemblyUpa(String inputAssemblyUpa) {
        this.inputAssemblyUpa = inputAssemblyUpa;
    }

    public SourmashLcaSummarizeParams withInputAssemblyUpa(String inputAssemblyUpa) {
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

    public SourmashLcaSummarizeParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("lca_search_db")
    public String getLcaSearchDb() {
        return lcaSearchDb;
    }

    @JsonProperty("lca_search_db")
    public void setLcaSearchDb(String lcaSearchDb) {
        this.lcaSearchDb = lcaSearchDb;
    }

    public SourmashLcaSummarizeParams withLcaSearchDb(String lcaSearchDb) {
        this.lcaSearchDb = lcaSearchDb;
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

    public SourmashLcaSummarizeParams withScaled(Long scaled) {
        this.scaled = scaled;
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
        return ((((((((((("SourmashLcaSummarizeParams"+" [inputAssemblyUpa=")+ inputAssemblyUpa)+", workspaceName=")+ workspaceName)+", lcaSearchDb=")+ lcaSearchDb)+", scaled=")+ scaled)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
