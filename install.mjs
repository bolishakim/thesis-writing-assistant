#!/usr/bin/env node

import { execSync } from "child_process";
import { existsSync, mkdirSync, cpSync } from "fs";
import { resolve, join, dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const args = process.argv.slice(2);
const command = args[0] || "install";

const SKILL_NAME = "thesis-writing-assistant";

// Skill source files (relative to this script)
const SKILL_FILES = [
  "SKILL.md",
  "scripts/academic_scorer.py",
  "references/ai-patterns.md",
  "references/academic-style.md",
  "references/section-guidelines.md",
  "references/audit-workflow.md",
  "references/latex-conventions.md",
  "references/professor-style-guide.md",
];

function printHelp() {
  console.log(`
\x1b[34m${SKILL_NAME}\x1b[0m — Claude skill for academic thesis writing

\x1b[33mUsage:\x1b[0m
  npx ${SKILL_NAME} install [options]
  npx ${SKILL_NAME} help

\x1b[33mOptions:\x1b[0m
  --global, -g    Install to ~/.claude/skills/ (available everywhere)
  --local, -l     Install to ./.claude/skills/ (current project only, default)

\x1b[33mExamples:\x1b[0m
  npx ${SKILL_NAME} install           # Install for current project
  npx ${SKILL_NAME} install --global  # Install globally

\x1b[33mAfter installing:\x1b[0m
  Use trigger phrases in Claude: "humanize", "academic rewrite", "audit", "polish"
  `);
}

function install(global) {
  const baseDir = global
    ? join(process.env.HOME, ".claude", "skills")
    : join(process.cwd(), ".claude", "skills");

  const targetDir = join(baseDir, SKILL_NAME);

  console.log();
  console.log(`\x1b[34mInstalling ${SKILL_NAME}...\x1b[0m`);
  console.log(`  Target: ${targetDir}`);
  console.log();

  // Create directories
  for (const subdir of ["scripts", "references"]) {
    const dir = join(targetDir, subdir);
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
  }

  // Copy skill files
  let copied = 0;
  for (const file of SKILL_FILES) {
    const src = join(__dirname, file);
    const dest = join(targetDir, file);

    if (existsSync(src)) {
      // Ensure parent directory exists
      const parentDir = dirname(dest);
      if (!existsSync(parentDir)) {
        mkdirSync(parentDir, { recursive: true });
      }
      cpSync(src, dest, { force: true });
      console.log(`  \x1b[32m✓\x1b[0m ${file}`);
      copied++;
    } else {
      console.log(`  \x1b[31m✗\x1b[0m ${file} (not found in package)`);
    }
  }

  console.log();
  console.log(`\x1b[32mInstalled ${copied} files.\x1b[0m`);
  console.log();
  console.log(`\x1b[33mTrigger phrases:\x1b[0m`);
  console.log(`  "humanize"          → Full rewrite (4 phases)`);
  console.log(`  "academic rewrite"  → Full rewrite (4 phases)`);
  console.log(`  "polish" / "clean up" → Quick polish`);
  console.log(`  "audit" / "score"   → Audit only`);
  console.log(`  "refine [section]"  → Section-specific rewrite`);
  console.log();
  console.log(`\x1b[33mScorer:\x1b[0m`);
  console.log(`  python ${join(targetDir, "scripts", "academic_scorer.py")} <file.tex>`);
  console.log();
}

switch (command) {
  case "install":
    const isGlobal = args.includes("--global") || args.includes("-g");
    install(isGlobal);
    break;
  case "help":
  case "--help":
  case "-h":
    printHelp();
    break;
  default:
    console.log(`\x1b[31mUnknown command: ${command}\x1b[0m`);
    printHelp();
    process.exit(1);
}
