
package us.kbase.kbsourmash;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: SourmashCompareParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "object_list",
    "workspace_name",
    "scaled"
})
public class SourmashCompareParams {

    @JsonProperty("object_list")
    private List<String> objectList;
    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("scaled")
    private Long scaled;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("object_list")
    public List<String> getObjectList() {
        return objectList;
    }

    @JsonProperty("object_list")
    public void setObjectList(List<String> objectList) {
        this.objectList = objectList;
    }

    public SourmashCompareParams withObjectList(List<String> objectList) {
        this.objectList = objectList;
        return this;
    }

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public SourmashCompareParams withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
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

    public SourmashCompareParams withScaled(Long scaled) {
        this.scaled = scaled;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((("SourmashCompareParams"+" [objectList=")+ objectList)+", workspaceName=")+ workspaceName)+", scaled=")+ scaled)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
