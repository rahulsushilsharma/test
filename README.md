I apologize for the confusion. Since you're using TypeScript with React, you might want to use `typescript` and `@typescript-eslint/parser` instead of `babel/parser` for parsing TypeScript files. Additionally, you can use `@typescript-eslint/parser` along with `@typescript-eslint/parser` for parsing TypeScript code.

Here's an updated example:

1. Install the required packages:

```bash
npm install typescript @typescript-eslint/parser @typescript-eslint/traverse
```

2. Modify the script accordingly:

```javascript
const fs = require('fs');
const path = require('path');
const { parse } = require('@typescript-eslint/parser');
const traverse = require('@typescript-eslint/traverse').traverse;

// Function to extract static strings from a file
function extractStringsFromFile(filePath, strings) {
  const code = fs.readFileSync(filePath, 'utf-8');
  const ast = parse(code, { sourceType: 'module', ecmaVersion: 2020, jsx: true });

  traverse(ast, {
    Literal(path) {
      if (typeof path.node.value === 'string') {
        strings.push(path.node.value);
      }
    },
  });
}

// Function to traverse through the project directory
function traverseDirectory(directoryPath, strings) {
  const files = fs.readdirSync(directoryPath);

  files.forEach(file => {
    const filePath = path.join(directoryPath, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      traverseDirectory(filePath, strings);
    } else if (stat.isFile() && filePath.endsWith('.tsx')) {
      extractStringsFromFile(filePath, strings);
    }
  });
}

// Main function to extract and save strings to a JSON file
function extractAndSaveStrings(directoryPath, outputPath) {
  const strings = [];
  traverseDirectory(directoryPath, strings);

  const jsonString = JSON.stringify({ strings }, null, 2);
  fs.writeFileSync(outputPath, jsonString);

  console.log('Static strings extracted and saved to', outputPath);
}

// Usage
const projectDirectory = '/path/to/your/project';
const outputJsonFile = '/path/to/output/strings.json';

extractAndSaveStrings(projectDirectory, outputJsonFile);
```

This script uses `@typescript-eslint/parser` for parsing TypeScript files and `@typescript-eslint/traverse` for traversing the AST. Make sure to adjust the paths and customize the script according to your project structure.
