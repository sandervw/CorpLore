import { readFileSync, writeFileSync } from "fs";
import { llmPrompt } from "./modules/llmPrompt.js";

const inputFile = readFileSync("../Input/input.md", "utf-8");

const prompt = `Write prompt here`;
const response = await llmPrompt(prompt);
console.log(response);

writeFileSync(`../Output/llmresult.md`, response);