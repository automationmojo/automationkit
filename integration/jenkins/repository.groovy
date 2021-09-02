import com.cloudbees.hudson.plugins.folder.Folder
import jenkins.model.Jenkins
import groovy.json.JsonSlurper

def get = new URL("https://httpbin.org/get").openConnection();
def getRC = get.getResponseCode();
println(getRC);
if(getRC.equals(200)) {
    println(get.getInputStream().getText());
}


GIT_REPOSITORY_URL="https://github.com/automationmojo/automationkit"
GIT_REPOSITORY_NAME="main"
GIT_APIKEY=""

GIT_REPOSITORY_URL_RAW = GIT_REPOSITORY_URL.split("//").with { it[0] + "//raw." + it[1] }

def jinst = Jenkins.instance
def branch_folder = jinst.getJob(GIT_REPOSITORY_NAME)

if(branch_folder == null) {
    branch_folder = jinst.createProject(Folder.class, GIT_REPOSITORY_NAME)
}

def jobmatrixUrl = new URL("$GIT_REPOSITORY_URL/integration/jenkins/jobmatrix.json").openConnection();

print (jobmatrixUrl)

def responseCode = jobmatrixUrl.getResponseCode()
if (responseCode == 200) {
    def jobmatrix  = new JsonSlurper().parse(branchUrl.newReader())
}
