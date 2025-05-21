const {ExecutionsClient} = require('@google-cloud/workflows');
const executionsClient = new ExecutionsClient();

exports.triggerWorkflow = async (req, res) => {
  const project = process.env.GCP_PROJECT || process.env.PROJECT_ID;
  const location = 'us-central1';
  const workflow = 'my-workflow'; // update to your workflow name

  const parent = `projects/${project}/locations/${location}/workflows/${workflow}`;

  try {
    const [execution] = await executionsClient.createExecution({
      parent,
      execution: {},
    });

    console.log(`Execution started: ${execution.name}`);
    res.status(200).send(`Execution started: ${execution.name}`);
  } catch (err) {
    console.error('Error:', err);
    res.status(500).send('Failed to start workflow');
  }
};
