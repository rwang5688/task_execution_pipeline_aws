package com.rwang5688.dal;

//import java.util.Map;

public class Task {
    private String user_id;
    private String task_id;
    private String project_name;
    private String task_tool;
    //private Map<String, String> task_extra_options;
    private String task_fileinfo_json;
    private String task_fileinfo_json_url;
    private String task_preprocess_tar;
    private String task_preprocess_tar_url;
    private String task_source_code_zip;
    private String task_source_code_zip_url;
    private String task_status;
    private String task_dot_scan_log_tar;
    private String task_dot_scan_log_tar_url;
    private String task_scan_result_tar;
    private String task_scan_result_tar_url;
    private String task_summary_pdf;
    private String task_summary_pdf_url;
    private String task_issues_csv;
    private String task_issues_csv_url;
    private String submit_timestamp;
    private String update_timestamp;

    public String getUserId() {
        return this.user_id;
    }
    public void setUserId(String user_id) {
        this.user_id = user_id;
    }

    public String getTaskId() {
        return this.task_id;
    }
    public void setTaskId(String task_id) {
        this.task_id = task_id;
    }

    public String getProjectName() {
        return this.project_name;
    }
    public void setProjectName(String project_name) {
        this.project_name = project_name;
    }

    public String getTaskTool() {
        return this.task_tool;
    }
    public void setTaskTool(String task_tool) {
        this.task_tool = task_tool;
    }

    //public Map<String, String> getTaskExtraOptions() {
    //    return this.task_extra_options;
    //}
    //public void setTaskExtraOptions(Map<String, String> task_extra_options) {
    //    this.task_extra_options = task_extra_options;
    //}

    public String getTaskFileinfoJson() {
        return this.task_fileinfo_json;
    }
    public void setTaskFileinfoJson(String task_fileinfo_json) {
        this.task_fileinfo_json = task_fileinfo_json;
    }

    public String getTaskFileinfoJsonUrl() {
        return this.task_fileinfo_json_url;
    }
    public void setTaskFileinfoJsonUrl(String task_fileinfo_json_url) {
        this.task_fileinfo_json_url = task_fileinfo_json_url;
    }

    public String getTaskPreprocessTar() {
        return this.task_preprocess_tar;
    }
    public void setTaskPreprocessTar(String task_preprocess_tar) {
        this.task_preprocess_tar = task_preprocess_tar;
    }

    public String getTaskPreprocessTarUrl() {
        return this.task_preprocess_tar_url;
    }
    public void setTaskPreprocessTarUrl(String task_preprocess_tar_url) {
        this.task_preprocess_tar_url = task_preprocess_tar_url;
    }

    public String getTaskSourceCodeZip() {
        return this.task_source_code_zip;
    }
    public void setTaskSourceCodeZip(String task_source_code_zip) {
        this.task_source_code_zip = task_source_code_zip;
    }

    public String getTaskSourceCodeZipUrl() {
        return this.task_source_code_zip_url;
    }
    public void setTaskSourceCodeZipUrl(String task_source_code_zip_url) {
        this.task_source_code_zip_url = task_source_code_zip_url;
    }

    public String getTaskStatus() {
        return this.task_status;
    }
    public void setTaskStatus(String task_status) {
        this.task_status = task_status;
    }

    public String getTaskDotScanLogTar() {
        return this.task_dot_scan_log_tar;
    }
    public void setTaskDotScanLogTar(String task_dot_scan_log_tar) {
        this.task_dot_scan_log_tar = task_dot_scan_log_tar;
    }

    public String getTaskDotScanLogTarUrl() {
        return this.task_dot_scan_log_tar_url;
    }
    public void setTaskDotScanLogTarUrl(String task_dot_scan_log_tar_url) {
        this.task_dot_scan_log_tar_url = task_dot_scan_log_tar_url;
    }

    public String getTaskScanResultTar() {
        return this.task_scan_result_tar;
    }
    public void setTaskScanResultTar(String task_scan_result_tar) {
        this.task_scan_result_tar = task_scan_result_tar;
    }

    public String getTaskScanResultTarUrl() {
        return this.task_scan_result_tar_url;
    }
    public void setTaskScanResultTarUrl(String task_scan_result_tar_url) {
        this.task_scan_result_tar_url = task_scan_result_tar_url;
    }

    public String getTaskSummaryPdf() {
        return this.task_summary_pdf;
    }
    public void setTaskSummaryPdf(String task_summary_pdf) {
        this.task_summary_pdf = task_summary_pdf;
    }

    public String getTaskSummaryPdfUrl() {
        return this.task_summary_pdf_url;
    }
    public void setTaskSummaryPdfUrl(String task_summary_pdf_url) {
        this.task_summary_pdf_url = task_summary_pdf_url;
    }

    public String getTaskIssuesCsv() {
        return this.task_issues_csv;
    }
    public void setTaskIssuesCsv(String task_issues_csv) {
        this.task_issues_csv = task_issues_csv;
    }

    public String getTaskIssuesCsvUrl() {
        return this.task_issues_csv_url;
    }
    public void setTaskIssuesCsvUrl(String task_issues_csv_url) {
        this.task_issues_csv_url = task_issues_csv_url;
    }

    public String getSubmitTimestamp() {
        return this.submit_timestamp;
    }
    public void setSubmitTimestamp(String submit_timestamp) {
        this.submit_timestamp = submit_timestamp;
    }

    public String getUpdateTimestamp() {
        return this.update_timestamp;
    }
    public void setUpdateTimestamp(String update_timestamp) {
        this.update_timestamp = update_timestamp;
    }

    private String toStringTemplate = null;

    public String toString() {
        if (this.toStringTemplate == null) {
            this.toStringTemplate = "Task [user_id=%s, task_id=%s, ";
            this.toStringTemplate += "project_name=%s, ";
            this.toStringTemplate += "task_tool=%s, "; //"task_extra_options=%s, ";
            this.toStringTemplate += "task_fileinfo_json=%s, task_fileinfo_json_url=%s, ";
            this.toStringTemplate += "task_preprocess_tar=%s, task_preprocess_tar_url=%s, ";
            this.toStringTemplate += "task_source_code_zip=%s, task_source_code_zip_url=%s, ";
            this.toStringTemplate += "task_status=%s, ";
            this.toStringTemplate += "task_dot_scan_log_tar=%s, task_dot_scan_log_tar_url=%s, ";
            this.toStringTemplate += "task_scan_result_tar=%s, task_scan_result_tar_url=%s, ";
            this.toStringTemplate += "task_summary_pdf=%s, task_summary_pdf_url=%s, ";
            this.toStringTemplate += "task_issues_csv=%s, task_issues_csv_url=%s, ";
            this.toStringTemplate += "submit_timestmp=%s, update_timestamp=%s]";
        }

        return String.format(toStringTemplate,
                            this.user_id, this.task_id,
                            this.project_name,
                            this.task_tool, //this.task_extra_options.toString(),
                            this.task_fileinfo_json, this.task_fileinfo_json_url,
                            this.task_preprocess_tar, this.task_preprocess_tar_url,
                            this.task_source_code_zip, this.task_source_code_zip_url,
                            this.task_status,
                            this.task_dot_scan_log_tar, this.task_dot_scan_log_tar_url,
                            this.task_scan_result_tar, this.task_scan_result_tar_url,
                            this.task_summary_pdf, this.task_summary_pdf_url,
                            this.task_issues_csv, this.task_issues_csv_url,
                            this.submit_timestamp, this.update_timestamp);
    }
}
