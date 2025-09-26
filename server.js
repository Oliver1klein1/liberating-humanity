const express = require('express');
const path = require('path');
const app = express();

// Serve static files from the epub/OEBPS directory
app.use(express.static(path.join(__dirname, 'epub/OEBPS')));

// Set correct MIME type for XHTML files
app.use((req, res, next) => {
  if (req.path.endsWith('.xhtml')) {
    res.type('application/xhtml+xml');
  }
  next();
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
