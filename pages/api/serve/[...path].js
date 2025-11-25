import fs from 'fs';
import path from 'path';

export default async function handler(req, res) {
  const { path: filePath } = req.query;
  
  // Join the path segments
  const requestedPath = Array.isArray(filePath) ? filePath.join('/') : filePath || 'index.html';
  
  // Construct the full file path
  const fullPath = path.join(process.cwd(), 'epub', 'OEBPS', requestedPath);
  
  // Security check: ensure the path is within the epub/OEBPS directory
  const epubPath = path.join(process.cwd(), 'epub', 'OEBPS');
  const resolvedPath = path.resolve(fullPath);
  const resolvedEpubPath = path.resolve(epubPath);
  
  if (!resolvedPath.startsWith(resolvedEpubPath)) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  try {
    console.log('Serving file:', resolvedPath);
    // Check if file exists
    if (!fs.existsSync(resolvedPath)) {
      return res.status(404).json({ error: 'File not found' });
    }
    
    const stats = fs.statSync(resolvedPath);
    
    // If it's a directory, try to serve index.html
    if (stats.isDirectory()) {
      const indexPath = path.join(resolvedPath, 'index.html');
      if (fs.existsSync(indexPath)) {
        const content = fs.readFileSync(indexPath, 'utf8');
        return res.status(200).setHeader('Content-Type', 'text/html').send(content);
      }
      return res.status(404).json({ error: 'Directory listing not allowed' });
    }
    
    // Determine content type
    let contentType = 'text/html';
    const isBinary = requestedPath.match(/\.(jpg|jpeg|png|gif|svg|ico|woff|woff2|ttf|eot)$/i);
    
    if (requestedPath.endsWith('.xhtml')) {
      contentType = 'application/xhtml+xml';
    } else if (requestedPath.endsWith('.css')) {
      contentType = 'text/css';
    } else if (requestedPath.endsWith('.js')) {
      contentType = 'application/javascript';
    } else if (requestedPath.endsWith('.jpg') || requestedPath.endsWith('.jpeg')) {
      contentType = 'image/jpeg';
    } else if (requestedPath.endsWith('.png')) {
      contentType = 'image/png';
    } else if (requestedPath.endsWith('.gif')) {
      contentType = 'image/gif';
    } else if (requestedPath.endsWith('.svg')) {
      contentType = 'image/svg+xml';
    }
    
    // Read and serve the file (binary for images, text for others)
    if (isBinary) {
      const content = fs.readFileSync(resolvedPath);
      return res.status(200).setHeader('Content-Type', contentType).send(content);
    } else {
      const content = fs.readFileSync(resolvedPath, 'utf8');
      return res.status(200).setHeader('Content-Type', contentType).send(content);
    }
  } catch (error) {
    console.error('Error serving file:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

