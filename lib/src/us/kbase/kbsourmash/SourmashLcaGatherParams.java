
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
 * <p>Original spec-file type: SourmashLcaGatherParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_assembly_upa",
    "workspace_name",
    "lca_search_db",
    "track_abundance"
})
public class SourmashLcaGatherParams {

    @JsonProperty("input_assembly_upa")
    private String inputAssemblyUpa;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("lca_search_db")
    private String lcaSearchDb;
    @JsonProperty("track_abundance")
    private Long trackAbundance;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_assembly_upa")
    public String getInputAssemblyUpa() {
        return inputAssemblyUpa;
    }

    @JsonProperty("input_assembly_upa")
    public void setInputAssemblyUpa(String inputAssemblyUpa) {
        this.inputAssemblyUpa = inputAssemblyUpa;
    }

    public SourmashLcaGatherParams withInputAssemblyUpa(String inputAssemblyUpa) {
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

    public SourmashLcaGatherParams withWorkspaceName(String workspaceName) {
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

    public SourmashLcaGatherParams withLcaSearchDb(String lcaSearchDb) {
        this.lcaSearchDb = lcaSearchDb;
        return this;
    }

    @JsonProperty("track_abundance")
    public Long getTrackAbundance() {
        return trackAbundance;
    }

    @JsonProperty("track_abundance")
    public void setTrackAbundance(Long trackAbundance) {
        this.trackAbundance = trackAbundance;
    }

    public SourmashLcaGatherParams withTrackAbundance(Long trackAbundance) {
        this.trackAbundance = trackAbundance;
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
        return ((((((((((("SourmashLcaGatherParams"+" [inputAssemblyUpa=")+ inputAssemblyUpa)+", workspaceName=")+ workspaceName)+", lcaSearchDb=")+ lcaSearchDb)+", trackAbundance=")+ trackAbundance)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
