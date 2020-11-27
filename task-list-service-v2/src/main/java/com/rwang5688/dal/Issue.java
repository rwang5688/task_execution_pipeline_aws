package com.rwang5688.dal;

public class Issue {
    private String task_id;
    private Integer task_issue_number;
    private String issue_key;
    private String issue_certainty;
    private Integer issue_complexity;
    private String file_path;
    private Integer start_line_no;
    private Integer start_column_no;
    private String function_name;
    private String variable_name;
    private String rule_set;
    private String rule_code;
    private String error_code;
    private String message;

    public String getTaskId() {
        return this.task_id;
    }
    public void setTaskId(String task_id) {
        this.task_id = task_id;
    }

    public Integer getTaskIssueNumber() {
        return this.task_issue_number;
    }
    public void setTaskIssueNumber(Integer task_issue_number) {
        this.task_issue_number = task_issue_number;
    }

    public String getIssueKey() {
        return this.issue_key;
    }
    public void setIssueKey(String issue_key) {
        this.issue_key = issue_key;
    }

    public String getIssueCertainty() {
        return this.issue_certainty;
    }
    public void setIssueCertainty(String issue_certainty) {
        this.issue_certainty = issue_certainty;
    }

    public Integer getIssueComplexity() {
        return this.issue_complexity;
    }
    public void setIssueComplexity(Integer issue_complexity) {
        this.issue_complexity = issue_complexity;
    }

    public String getFilePath() {
        return this.file_path;
    }
    public void setFilePath(String file_path) {
        this.file_path = file_path;
    }

    public Integer getStartLineNo() {
        return this.start_line_no;
    }
    public void setStartLineNo(Integer start_line_no) {
        this.start_line_no = start_line_no;
    }

    public Integer getStartColumnNo() {
        return this.start_column_no;
    }
    public void setStartColumnNo(Integer start_column_no) {
        this.start_column_no = start_column_no;
    }

    public String getFunctionName() {
        return this.function_name;
    }
    public void setFunctionName(String function_name) {
        this.function_name = function_name;
    }

    public String getVariableName() {
        return this.variable_name;
    }
    public void setVariableName(String variable_name) {
        this.variable_name = variable_name;
    }

    public String getRuleSet() {
        return this.rule_set;
    }
    public void setRuleSet(String rule_set) {
        this.rule_set = rule_set;
    }

    public String getRuleCode() {
        return this.rule_code;
    }
    public void setRuleCode(String rule_code) {
        this.rule_code = rule_code;
    }

    public String getErrorCode() {
        return this.error_code;
    }
    public void setErrorCode(String error_code) {
        this.error_code = error_code;
    }

    public String getMessage() {
        return this.message;
    }
    public void setMessage(String message) {
        this.message = message;
    }

    private String toStringTemplate = null;

    public String toString() {
        if (this.toStringTemplate == null) {
            this.toStringTemplate = "Issue [task_id=%s, task_issue_number=%d, ";
            this.toStringTemplate += "issue_key=%s, issue_certainty=%s, issue_complexity=%d, ";
            this.toStringTemplate += "file_path=%s, start_line_no=%d, start_column_no=%d, ";
            this.toStringTemplate += "function_name=%s, variable_name=%s, ";
            this.toStringTemplate += "rule_set=%s, rule_code=%s, ";
            this.toStringTemplate += "error_code=%s, message=%s]";
        }

        return String.format(toStringTemplate,
                            this.task_id, this.task_issue_number,
                            this.issue_key, this.issue_certainty, this.issue_complexity,
                            this.file_path, this.start_line_no, this.start_column_no,
                            this.function_name, this.variable_name,
                            this.rule_set, this.rule_code,
                            this.error_code, this.message);
    }
}
