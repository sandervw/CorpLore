import Anthropic from "@anthropic-ai/sdk";

const llmPrompt = async (message) => {

  const client = new Anthropic();

  // Use 'claude-sonnet-4-5-20250929' for speed/cost balance
  // Use 'claude-opus-4-5-20251101' for highest quality
  const MODEL = 'claude-opus-4-5-20251101';
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 20000,
    messages: [
      {
        role: "user",
        content: message,
      },
    ],
  });
  return response.content[0].text.trim();

};

export { llmPrompt };