/*
    __author__ = "Myron Walker"
    __copyright__ = "Copyright 2020, Myron W Walker"
    __credits__ = []
    __version__ = "1.0.0"
    __maintainer__ = "Myron Walker"
    __email__ = "myron.walker@gmail.com"
    __status__ = "Development" # Prototype, Development or Production
    __license__ = "MIT"
*/

// Summary State
var g_summary = null;

// Configuration State
var g_startup_configuration = null;

// Results State
var g_results = null;
var g_counter_passed = 0;
var g_counter_failed = 0;
var g_counter_errors = 0;
var g_counter_skipped = 0;
var g_counter_total = 0;
var g_display_mode = "LIST";
var g_filter_mode = "NONE";

// Artifacts State
var g_artifacts_catalog = null;
var g_artifacts_sub_catalogs = null;
var g_artifacts_buttons = null;
var g_artifacts_tabs = null;

// Import Error State
var g_import_errors = null;


// File Catalog State
var g_catalog = null;

/*************************************************************************************
 *************************************************************************************
 *
 *                                  HELPER FUNCTIONS
 * 
 *************************************************************************************
 *************************************************************************************/

function isDict(value) {
    rtnval = false;
    if (value.constructor == Object) {
        rtnval = true;
    }
    return rtnval
}

function isString(value) {
    rtnval = false;
    if (value.constructor == String) {
        rtnval = true;
    }
    return rtnval
}

async function load_http(url) {
    var promise = new Promise((resolve, reject) => {
        var xmlhttp = new XMLHttpRequest();
        
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    resolve(this.responseText);
                } else {
                    reject(this.statusText);
                }
            }
        };

        xmlhttp.onerror = function (){
            reject(this.statusText);
        };

        xmlhttp.open("GET", url, true);
        xmlhttp.send();

    });

    return promise;
}

async function load_json(url) {
    var promise = new Promise((resolve, reject) => {
        var xmlhttp = new XMLHttpRequest();
        
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    var robj = JSON.parse(this.responseText);
                    resolve(robj);
                } else {
                    reject(this.statusText);
                }
            }
        };

        xmlhttp.onerror = function (){
            reject(this.statusText);
        };

        xmlhttp.open("GET", url, true);
        xmlhttp.send();

    });

    return promise;
}

async function load_json_stream(url) {
    var promise = new Promise((resolve, reject) => {
        var xmlhttp = new XMLHttpRequest();
        
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    var json_objects = [];

                    var split_responses = this.responseText.split("\30");
                    var srlength = split_responses.length;
                    while (srlength > 0) {
                        var ritem = split_responses.pop();
                        if (ritem.length > 0) {
                            var robj = JSON.parse(ritem);
                            json_objects.unshift(robj);
                        }
                        srlength = srlength - 1;
                    }

                    resolve(json_objects);
                } else {
                    reject(this.statusText);
                }
            }
        };

        xmlhttp.onerror = function (){
            reject(this.statusText);
        };

        xmlhttp.open("GET", url, true);
        xmlhttp.send();

    });

    return promise;
}

/*************************************************************************************
 *************************************************************************************
 *
 *                                  ENABLE FUNCTIONS
 * 
 *************************************************************************************
 *************************************************************************************/

function enable_artifacts_section() {
    document.getElementById('artifacts-title').style = "display: block";
    document.getElementById('artifacts-tab-bar').style = "display: block";
    document.getElementById('artifacts-tab-content').style = "display: block";
}

/*************************************************************************************
 *************************************************************************************
 *
 *                                   LOAD FUNCTIONS
 * 
 *************************************************************************************
 *************************************************************************************/

async function load_artifact_folders()
{
    g_artifacts_catalog = await load_json("artifacts/catalog.json");

    if ((g_artifacts_catalog != null) && (g_artifacts_catalog.folders.length > 0)) {
        enable_artifacts_section();

        g_artifacts_sub_catalogs = {};

        for (var findex in g_artifacts_catalog.folders) {
            var folder = g_artifacts_catalog.folders[findex];

            artifact_catalog = await load_http("artifacts/" + folder + "/catalog.json").catch(err => {
                console.log("The '" + folder + "' artifacts folder does not have a 'catalog.json' file.")
            });

            if ((artifact_catalog != null) && (artifact_catalog != "")) {
                g_artifacts_sub_catalogs[folder] = artifact_catalog;
            }
        }
    }
}

async function load_catalog() {
    g_catalog = await load_json("catalog.json");
}

async function load_configuration() {
    g_startup_configuration = {}

    var landscape = await load_json("landscape-declared.json").catch(err => {
        console.log("Unable to load the landscape declaration file='landscape-declared.json'.")
    });
    var startup = await load_json("startup-configuration.json").catch(err => {
        console.log("Unable to load the landscape declaration file='startup-configuration.json'.")
    });

    g_startup_configuration["landscape"] = landscape;
    g_startup_configuration["startup"] = startup;

    var upnp_startup_scan = await load_json("landscape-startup-scan.json").catch(err => {
        console.log("Unable to load the landscape declaration file='landscape-startup-scan.json'.")
    });

    startup["scans"] = upnp_startup_scan;
}

async function load_import_errors() {
    g_import_errors = await load_json_stream("import_errors.jsos")
}

async function load_results() {
    var results = await load_json_stream("testrun_results.jsos");

    var counter_passed = 0;
    var counter_errors = 0;
    var counter_failed = 0;
    var counter_skipped = 0;

    if (g_display_mode == "LIST") {
        g_results = [];

        if (g_filter_mode == "NONE") {
            var rcount = results.length;
            while(rcount > 0) {
                var ritem = results.shift();
                if (ritem.rtype == "TEST") {
                    var detail = ritem.detail;

     detail.passed = false;
     detail.skipped = false;

                    if (detail.errors.length > 0) {
                        counter_errors += 1;
                    }
                    else if (detail.failures.length > 0) {
                        counter_failed += 1;
                    }
                    else {
                        if (ritem.result == "SKIPPED") {
                            detail.skipped = true;
                            counter_skipped += 1;
                        } else {
                           detail.passed = true;
                           counter_passed += 1;
                        }
                    }

                    g_results.push(ritem);
                }

                rcount = rcount - 1;
            }
        } else {
            var filter_status = g_filter_mode;
            var rcount = results.length;
            while(rcount > 0) {
                var ritem = results.shift();
                if ((ritem.rtype == "TEST") && (ritem.result == filter_status)) {
                    g_results.push(ritem);
                }
                rcount = rcount - 1;
            }
        }
    } else {
        //TODO: Add code to create tree based g_results
    }

    g_counter_passed = counter_passed;
    g_counter_errors = counter_errors;
    g_counter_failed = counter_failed;
    g_counter_skipped = counter_skipped;

}

async function load_summary() {
    g_summary = await load_json("testrun_summary.json");
}

/*************************************************************************************
 *************************************************************************************
 *
 *                                 ELEMENT CREATION
 * 
 *************************************************************************************
 *************************************************************************************/

function adjust_index_identifier(path, name, value) {
    var display_name = name;

    var modpath = path.join("/")
    if (modpath == "landscape/environment/credentials") {
        display_name = display_name + " - " + value["identifier"];
    } else if (modpath == "landscape/pod/devices") {
        var devtype = value["deviceType"];
        if (devtype == "network/upnp") {
            var upnpinfo = value["upnp"];
            display_name = display_name + " - " + upnpinfo["modelNumber"] + ", " + upnpinfo["modelName"] + " - " + upnpinfo["IP"] + " - " + upnpinfo["USN"];
        } else if (devtype == "network/ssh") {
            display_name = display_name + " - " + value["host"];
        }
        
    } else if ((modpath == "landscape/pod/power") || (modpath == "landscape/pod/serial")) {
        display_name = display_name + " - " + value["name"]
    } else if ((modpath == "startup/scans/upnp/found_devices") ||
               (modpath == "startup/scans/upnp/matching_devices") ||
               (modpath == "startup/scans/upnp/missing_devices")) {
        display_name = display_name + " - " + value["IP"];
        var usn = value["USN"];
        if (usn != undefined) {
            display_name = display_name +  " - " + usn;
        }
    } else if ((modpath == "startup/scans/ssh/matching_devices") ||
               (modpath == "startup/scans/ssh/missing_devices")) {
        var devtype = value["deviceType"];
        if (devtype == "network/upnp") {
            var upnpinfo = value["upnp"];
            display_name = display_name + " - " + value["host"] + " - " + upnpinfo["modelNumber"] + ", " + upnpinfo["modelName"] + " - " + upnpinfo["USN"];
        } else if (devtype == "network/ssh") {
            display_name = display_name + " - " + value["host"];
        }
    }


    return display_name;
}

function append_configuration_array_items(bodyElement, arrayItems, path=[]) {
    arrayItems.forEach( kvpair => {
        const [key, value] = kvpair;
        append_configuration_array_node(bodyElement, key, value, path);
    });
}

function append_configuration_dict_items(bodyElement, dictItems, path=[]) {
    dictItems.forEach( kvpair => {
        const [key, value] = kvpair;
        var displayname = adjust_index_identifier(path, key, value);
        var childNode = create_configuration_tree_node(displayname, value, path);
        bodyElement.appendChild(childNode);
    });
}

function append_configuration_table(bodyElement, rowItems, path=[]) {

    var tableElement = document.createElement("table");
    tableElement.classList.add("tree-node-table");

    rowItems.forEach( kvpair => {
        const [key, value] = kvpair;

        var rowElement = document.createElement("tr");
        rowElement.classList.add("tree-node-row");

        var keyElement = document.createElement("td");
        keyElement.classList.add("tree-node-key");
        keyElement.innerHTML = key;

        var valElement = document.createElement("td");
        valElement.classList.add("tree-node-val");
        valElement.innerHTML = value;

        rowElement.appendChild(keyElement);
        rowElement.appendChild(valElement);
        tableElement.appendChild(rowElement);
    });

    bodyElement.appendChild(tableElement);
}

function append_configuration_array_node(bodyElement, name, adata, path=[]) {

    path.push(name);

    var nodeElement = document.createElement("details");
    nodeElement.classList.add("tree-node");

    var nodeElementTitle = document.createElement("summary");
    nodeElementTitle.classList.add("tree-node-hdr");
    nodeElementTitle.innerHTML = name;
    nodeElement.appendChild(nodeElementTitle);

    var nodeElementBody = document.createElement("div");
    nodeElementBody.classList.add("tree-node-body")
    nodeElement.appendChild(nodeElementBody);

    var arrayItems = [];
    var dictItems = [];
    var rowItems = [];

    for (var index in adata) {
        var item = adata[index];
        if (isString(item)) {
            rowItems.push([index, item]);
        } else if (Array.isArray(item)) {
            arrayItems.push([index, item]);
        } else if (isDict(item)) {
            dictItems.push([index, item]);
        } else {
            rowItems.push([index, item]);
        }
    };

    if (rowItems.length > 0) {
        append_configuration_table(nodeElementBody, rowItems, path);
    }

    if (arrayItems.length > 0) {
        append_configuration_array_items(nodeElementBody, arrayItems, path);
    }

    if (dictItems.length > 0) {
        append_configuration_dict_items(nodeElementBody, dictItems, path);
    }

    bodyElement.appendChild(nodeElement);

    path.pop();

}

function create_configuration_tree_node(name, ndata, path=[]) {

    path.push(name);

    var nodeElement = document.createElement("details");
    nodeElement.classList.add("tree-node");

    var nodeElementTitle = document.createElement("summary");
    nodeElementTitle.classList.add("tree-node-hdr");
    nodeElementTitle.innerHTML = name;
    nodeElement.appendChild(nodeElementTitle);

    var nodeElementBody = document.createElement("div");
    nodeElementBody.classList.add("tree-node-body")
    nodeElement.appendChild(nodeElementBody);

    var arrayItems = [];
    var dictItems = [];
    var rowItems = [];

    for (const [key, value] of Object.entries(ndata)) {
        if (value != null) {
            if (isString(value)) {
                rowItems.push([key, value]);
            } else if (Array.isArray(value)) {
                arrayItems.push([key, value]);
            } else if (isDict(value)) {
                dictItems.push([key, value]);
            } else {
                rowItems.push([key, value]);
            }
        } else {
            console.log("Null value encountered key=" + key + " .");
        }

    }

    if (rowItems.length > 0) {
        append_configuration_table(nodeElementBody, rowItems, path);
    }

    if (arrayItems.length > 0) {
        append_configuration_array_items(nodeElementBody, arrayItems, path);
    }

    if (dictItems.length > 0) {
        append_configuration_dict_items(nodeElementBody, dictItems, path);
    }

    path.pop();

    return nodeElement;
}

function create_failures_table(failuresList) {
    failuresTable = document.createElement("div");
    failuresTable.classList.add("f-list");
    for (var fidx in failuresList) {
        var fitem = failuresList[fidx];
        var preElement = document.createElement("pre");
        var msg = "";
        for (var lidx in fitem) {
            var lstr = fitem[lidx];
            msg = msg + lstr + "\n";
        }
        preElement.innerHTML = msg;
        failuresTable.appendChild(preElement);
    }

    return failuresTable
}

function create_result_item_content(ritem) {
    var resultElement = document.createElement("details");
    resultElement.classList.add("ritem-row");
    var summaryContainer = document.createElement("summary");
    summaryContainer.classList.add("ritem-hdr")

    var summaryStart = document.createElement("div");
    summaryStart.innerHTML = ritem.start;
    summaryStart.classList.add("ritem-hdr-start");
    summaryContainer.appendChild(summaryStart);

    var summaryName = document.createElement("div");
    summaryName.innerHTML = ritem.name;
    summaryName.classList.add("ritem-hdr-name");
    summaryContainer.appendChild(summaryName);

    var detail = ritem.detail;

    var error_count = detail.errors.length;
    var failure_count = detail.failures.length;
    var skip_count = detail.skipped ? 1 : 0;
    var pass_count = detail.passed ? 1 : 0;

    var summaryE = document.createElement("div");
    summaryE.innerHTML = error_count;
    summaryE.classList.add(error_count > 0 ? "ritem-hdr-e" : "ritem-hdr-z");
    summaryContainer.appendChild(summaryE);

    var summaryF = document.createElement("div");
    summaryF.innerHTML = failure_count;
    summaryF.classList.add(failure_count > 0 ? "ritem-hdr-f" : "ritem-hdr-z");
    summaryContainer.appendChild(summaryF);

    var summaryS = document.createElement("div");
    summaryS.innerHTML = skip_count;
    summaryS.classList.add(skip_count > 0 ? "ritem-hdr-s" : "ritem-hdr-z");
    summaryContainer.appendChild(summaryS);

    var summaryP = document.createElement("div");
    summaryP.innerHTML = pass_count;
    summaryP.classList.add(pass_count > 0 ? "ritem-hdr-p" : "ritem-hdr-z");
    summaryContainer.appendChild(summaryP);

    var detailContainer = document.createElement("div");
    detailContainer.classList.add("dtl-body");
    detailContainer.appendChild(document.createElement("br"));

    var otherDetail = document.createElement("div");
    otherDetail.classList.add("dtl-hdr-row");

    var stopLabel = document.createElement("div");
    stopLabel.innerHTML = "Stop";
    stopLabel.classList.add("dtl-hdr-stop-l");
    otherDetail.appendChild(stopLabel);
    var stopValue = document.createElement("div");
    stopValue.innerHTML = ritem.stop;
    stopValue.classList.add("dtl-hdr-stop-v");
    otherDetail.appendChild(stopValue);

    var instLabel = document.createElement("div");
    instLabel.innerHTML = "InstId";
    instLabel.classList.add("dtl-hdr-inst-l");
    otherDetail.appendChild(instLabel);
    var instValue = document.createElement("div");
    instValue.classList.add("dtl-hdr-inst-v");
    instValue.innerHTML = ritem.instance;
    otherDetail.appendChild(instValue);

    detailContainer.appendChild(otherDetail);
    detailContainer.appendChild(document.createElement("br"));

    if (detail.hasOwnProperty("documentation")) {
        var docsHeader = document.createElement("h3");
        docsHeader.classList.add("doc-hdr");
        docsHeader.innerHTML = "DOCUMENTATION"
        detailContainer.appendChild(docsHeader);
        
        var docContent = document.createElement("pre");
        docContent.classList.add("doc-content");
        docContent.innerHTML = detail.documentation;
        detailContainer.appendChild(docContent);
    }

    if (detail.errors.length > 0) {
        var errorList =  detail.errors;
        var errorsHeader = document.createElement("h3");
        errorsHeader.classList.add("e-list-hdr");

        errorsHeader.innerHTML = "ERRORS";
        detailContainer.appendChild(errorsHeader);

        errorsTable = document.createElement("div");
        errorsTable.classList.add("e-list");
        for (var eidx in errorList) {
            var eitem = errorList[eidx];
            var preElement = document.createElement("pre");
            var msg = "";
            for (var lidx in eitem) {
                var lstr = eitem[lidx];
                msg = msg + lstr + "\n";
            }
            preElement.innerHTML = msg;
            errorsTable.appendChild(preElement);
        }
        detailContainer.appendChild(errorsTable);

        detailContainer.appendChild(document.createElement("br"));
    }

    if (detail.failures.length > 0) {
        var failuresList =  detail.failures;
        var failuresHeader = document.createElement("h3");
        failuresHeader.classList.add("f-list-hdr");

        failuresHeader.innerHTML = "FAILURES";
        detailContainer.appendChild(failuresHeader);

        var failuresTable = create_failures_table(failuresList);
        detailContainer.appendChild(failuresTable);

        detailContainer.appendChild(document.createElement("br"));
    }

    resultElement.appendChild(detailContainer);
    resultElement.appendChild(document.createElement("br"));

    resultElement.appendChild(summaryContainer);

    return resultElement;
}

function create_results_content_as_list() {
    var result_table_body = document.getElementById("test-results-body");
    for (var idx in g_results) {
        var ritem = g_results[idx];
        var eitem = create_result_item_content(ritem);
        result_table_body.appendChild(eitem);
    }
}

function create_results_content_as_tree() {
    
}

function select_tab(name) {
    var tabIndex = null;

    var tab_count = g_artifacts_buttons.length;
    var tindex = 0;
    while(tindex < tab_count) {
        var tabButton = g_artifacts_buttons[tindex];
        var buttonName = tabButton.getAttribute("name");
        if (buttonName == name) {
            tabIndex = tindex;
        }

        tindex += 1;
    }

    for (var tindex in g_artifacts_buttons) {
        var tabButton = g_artifacts_buttons[tindex];
        var buttonName = tabButton.getAttribute("name");
        if (buttonName == name) {
            tabIndex = tindex;
        }
    }

    if (tabIndex != null) {

        var tab_count = g_artifacts_buttons.length;
        var tindex = 0;
        while(tindex < tab_count) {
            var tabButton = g_artifacts_buttons[tindex];
            tabButton.classList.remove("active");

            var tabTab = g_artifacts_tabs[tindex];
            tabTab.style = "display: none;";

            tindex += 1;
        }

        var tabButton = g_artifacts_buttons[tabIndex];
        tabButton.classList.add("active");

        var tabContent = g_artifacts_tabs[tabIndex];
        tabContent.style = "display: block;";
    }
}

function on_tab_click(event) {
    var tabName = this.getAttribute("name");

    select_tab(tabName);
    console.log("Tab '" + tabName + "' clicked.")
}

function render_artifact_tab(tabBarContainer, tabContentContainer, name, contentUrl) {
    var tabButtonElement = document.createElement('button');
    tabButtonElement.setAttribute("name", name);
    tabButtonElement.innerHTML = name;
    tabButtonElement.classList.add("tab");
    tabButtonElement.onclick = on_tab_click;
    tabBarContainer.appendChild(tabButtonElement);

    g_artifacts_buttons.push(tabButtonElement);

    var tabContentElement = document.createElement('iframe');
    tabContentElement.src = contentUrl;
    tabContentElement.classList.add("tabcontent")
    tabContentContainer.appendChild(tabContentElement);

    g_artifacts_tabs.push(tabContentElement);
}

function render_import_error_item_content(container, imp_err_item) {

    var imp_err_item_row = document.createElement("details");
    imp_err_item_row.classList.add("ierr-item-hdr");

    var summary_item = document.createElement("summary");
    summary_item.classList.add('ierr-item-hdr');
    var filename_item = document.createElement('div');
    filename_item.classList.add('ierr-item-hdr-filename');
    filename_item.innerHTML = imp_err_item.filename;
    summary_item.appendChild(filename_item);

    var detail_body = document.createElement('div');
    detail_body.classList.add("dtl-body");

    var stack_trace_hdr = document.createElement('h3');
    stack_trace_hdr.classList.add('f-list-hdr');
    stack_trace_hdr.innerHTML = "Stack Trace";
    detail_body.appendChild(stack_trace_hdr);

    var st_list = document.createElement('div');
    st_list.classList.add('ff-list');
    detail_body.appendChild(st_list);

    var failuresTable = create_failures_table([imp_err_item.trace]);

    imp_err_item_row.appendChild(failuresTable);
    imp_err_item_row.appendChild(summary_item);

    container.appendChild(imp_err_item_row);

}

function render_file_element(container, name, ref) {
    var nxtRow = document.createElement("div");
    nxtRow.classList.add('ff-row');

    var iconCont = document.createElement("div");
    iconCont.classList.add('ff-icon');
    var imgElmnt = document.createElement("img");
    imgElmnt.classList.add("icon-file");
    iconCont.appendChild(imgElmnt);
    nxtRow.appendChild(iconCont);

    var linkCont = document.createElement("div");
    linkCont.classList.add('ff-name');
    var linkElmnt = document.createElement("a");
    linkElmnt.href = ref;
    linkElmnt.innerHTML = name;
    linkCont.appendChild(linkElmnt);
    nxtRow.appendChild(linkCont);

    container.appendChild(nxtRow);
}

function render_folder_element(container, name, ref) {

    var nxtRow = document.createElement("div");
    nxtRow.classList.add('ff-row');

    var iconCont = document.createElement("div");
    iconCont.classList.add('ff-icon');
    var imgElmnt = document.createElement("img");
    imgElmnt.classList.add("icon-folder");
    iconCont.appendChild(imgElmnt);
    nxtRow.appendChild(iconCont);

    var linkCont = document.createElement("div");
    linkCont.classList.add('ff-name');
    var linkElmnt = document.createElement("a");
    linkElmnt.href = ref;
    linkElmnt.innerHTML = name;
    linkCont.appendChild(linkElmnt);
    nxtRow.appendChild(linkCont);

    container.appendChild(nxtRow);

}

/*************************************************************************************
 *************************************************************************************
 *
 *                                   SECTION REFRESH
 * 
 *************************************************************************************
 *************************************************************************************/

function refresh_artifacts() {
    var artifactsBarElement = document.getElementById("artifacts-tab-bar");
    var artifactsContentElement = document.getElementById("artifacts-tab-content");

    g_artifacts_buttons = [];
    g_artifacts_tabs = [];

    for (var findex in g_artifacts_catalog.folders) {
        var folder = g_artifacts_catalog.folders[findex];
        var subCatalog = g_artifacts_sub_catalogs[folder];
        if (subCatalog != undefined) {
            var folderURL = "artifacts/" + folder + "/tab.html";
            render_artifact_tab(artifactsBarElement, artifactsContentElement, folder, folderURL);
        }
    }

    if (g_artifacts_buttons.length > 0) {
        var firstButton = g_artifacts_buttons[0];

        var tabName = firstButton.getAttribute("name");
        select_tab(tabName);
    }
}

function refresh_catalog() {

    var container = document.getElementById("container-folders");
    render_folder_element(container, "Parent", "..")

    var folders_list = g_catalog.folders;
    for (var idx in folders_list) {
        var nxt = folders_list[idx];

        render_folder_element(container, nxt, nxt)
    }

    var container = document.getElementById("container-files");
    var file_list = g_catalog.files;
    for (var idx in file_list) {
        var nxt = file_list[idx];

        render_file_element(container, nxt, nxt)
    }
}

function refresh_configuration() {
    var configurationBodyElement = document.getElementById("test-configuration-body");

    var landscapeNodeElement = create_configuration_tree_node("landscape", g_startup_configuration["landscape"]);
    configurationBodyElement.appendChild(landscapeNodeElement);

    var startupNodeElement = create_configuration_tree_node("startup", g_startup_configuration["startup"]);
    configurationBodyElement.appendChild(startupNodeElement);
}

function refresh_import_errors() {
    var ierrbody = document.getElementById("import-errors-body");

    for (var idx in g_import_errors) {
        var imp_err_item = g_import_errors[idx];
        render_import_error_item_content(ierrbody, imp_err_item);
    }
}

function refresh_summary() {
    if (g_summary.hasOwnProperty("title") && g_summary.title != null) {
        document.getElementById("summary-title").innerHTML = g_summary.title
    }
    if (g_summary.hasOwnProperty("build") && g_summary.build != null) {
        document.getElementById("summary-build").innerHTML = g_summary.build;
    }
    if (g_summary.hasOwnProperty("branch") && g_summary.branch != null) {
        document.getElementById("summary-branch").innerHTML = g_summary.branch;
    }
    if (g_summary.hasOwnProperty("flavor") && g_summary.flavor != null) {
        document.getElementById("summary-flavor").innerHTML = g_summary.flavor;
    }
    if (g_summary.hasOwnProperty("landscape") && g_summary.landscape != null) {
        document.getElementById("summary-landscape").innerHTML = g_summary.landscape;
    }
    if (g_summary.hasOwnProperty("start") && g_summary.start != null) {
        document.getElementById("summary-start").innerHTML = g_summary.start;
    }
    if (g_summary.hasOwnProperty("stop") && g_summary.stop != null) {
        document.getElementById("summary-stop").innerHTML = g_summary.stop;
    }
    if (g_summary.hasOwnProperty("result") && g_summary.result != null) {
        document.getElementById("summary-status").innerHTML = g_summary.result;
    }
    if (g_summary.hasOwnProperty("detail") && g_summary.detail != null) {
        detail = g_summary.detail;

        if (detail.hasOwnProperty("errors") && (detail.errors != null)) {
            g_counter_errors = detail.errors;
        }
        if (detail.hasOwnProperty("failed") && (detail.failed != null)) {
            g_counter_failed = detail.failed;
        }
        if (detail.hasOwnProperty("skipped") && (detail.skipped)) {
            g_counter_skipped = detail.skipped;
        }
        if (detail.hasOwnProperty("passed") && (detail.passed != null)) {
            g_counter_passed = detail.passed;
        }
        if (detail.hasOwnProperty("total") && (detail.total != null)) {
            g_counter_total = detail.total;
        } else {
            g_counter_total = g_counter_errors + g_counter_failed + g_counter_skipped + g_counter_passed;
        }
    }
    else {
        g_counter_total = g_counter_errors + g_counter_failed + g_counter_skipped + g_counter_passed;
    }

    var relevant_test_counter = (g_counter_total - g_counter_skipped);
    var summary_score = "(error)";
    if (relevant_test_counter > 0) {
        summary_score = (g_counter_passed / (g_counter_total - g_counter_skipped)) * 100;
    }

    document.getElementById("summary-error").innerHTML = g_counter_errors;
    document.getElementById("summary-fail").innerHTML = g_counter_failed;
    document.getElementById("summary-skip").innerHTML = g_counter_skipped;
    document.getElementById("summary-pass").innerHTML = g_counter_passed;
    document.getElementById("summary-total").innerHTML = g_counter_total;
    document.getElementById("summary-score").innerHTML = summary_score.toFixed(2);
}

/*************************************************************************************
 *************************************************************************************
 *
 *                                      PAGE LOAD
 * 
 *************************************************************************************
 *************************************************************************************/

async function refresh_page() {
    load_summary().then(() => {
        refresh_summary();
    });

    load_configuration().then(() => {
        refresh_configuration();
    });

    load_results().then(() => {
        var result_content = null;
    
        if (g_display_mode == "LIST") {
            result_content = create_results_content_as_list();
        } else {
            result_content = create_results_content_as_tree();
        }

        if (result_content != null) {
            var resultsContainer = document.getElementById("test-results-body");
            resultsContainer.innerHTML = "";
            resultsContainer.appendChild(result_content);
        }
    });

    load_import_errors().then(() => {
        refresh_import_errors();
    });

    load_catalog().then(() => {
        if (g_catalog.folders.indexOf("artifacts") > -1) {
            load_artifact_folders().then(() => {
                refresh_artifacts();
            });
        }

        refresh_catalog();
    });
}