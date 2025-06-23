# CS6620-CICD-Pipeline-p1
This is a HW assignment for CS6620 (Cloud Computing) at the Roux Institute at Northeastern. The goal was to set up a basic project that uses automated testing and Github Actions workflows. Many developers use this to make sure that their new code doesn't break anything in production. I chose to create a simple Pokemon-themed python module (Why you ask? because I looooove Pokemon) to show how the unit tests and automation work together. The scripts are very simple, only including a few basic battle simulating functions such as attacking and healing. The tests basically make sure that those functions are working properly.

Regarding the continuous integration requirement, the GitHub workflow runs the tests automatically whenever code is pushed, a pull request is opened, or the workflow is triggered manually. Test workflow can be triggered manually by going to the `Actions` tab and clicking on the `Run Workflow` button under the Pokemon Tests workflow. You can view the configuration in `.github/workflows/main.yml`.

Shown below is an image of a few workflow runs (on push and upon manual triggering) as proof that the workflow is running correctly:
<p float="left", align="center">
  <img src="figs/workflow_runs.png" width="500"/>
</p>

## Setup
You can run this project using either `pip` or `conda`. First make sure to properly clone and enter the repository. Alternatively, just make sure that your local environment contains `pytest` as a dependency.

### Using `pip`:
```bash
# Create/activate venv (optional)
python3 -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
PYTHONPATH=src pytest tests/
```

### Using `conda`:
```bash
# Create/activate the environment
conda env create -f environment.yml
conda activate cicd_pipeline_p1_env

# Run tests
PYTHONPATH=src pytest tests/
# Windows: set PYTHONPATH=src && pytest tests/
```

## References and AI Appendix
* GitHub documentation that goes over CI workflow with Python - https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-python
* DevOps Pipeline - https://www.atlassian.com/devops/devops-tools/devops-pipeline
* Continuous Integration vs. Delivery vs. Deployment - https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment
* Asking Claude to give me an explanation about GitHub workflows with bullet points along with a basic example of a typical workflow structure - https://claude.ai/share/dcdaff6e-feb2-4832-b0ad-6897e6855121