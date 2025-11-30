import fs from 'fs';
import path from 'path';
import Head from 'next/head';

export default function Home({ htmlContent, cssContent }) {
  if (!htmlContent) {
    return <div>Loading...</div>;
  }

  // Process HTML to update asset paths on the server side
  let processedHtml = htmlContent;
  // Update relative paths to use /epub/ prefix
  processedHtml = processedHtml.replace(/href=["']([^"']+)["']/g, (match, url) => {
    if (url.startsWith('http') || url.startsWith('/epub/') || url.startsWith('#')) {
      return match;
    }
    // Convert absolute paths starting with / to /epub/ (for xhtml files)
    if (url.startsWith('/') && (url.endsWith('.xhtml') || url.endsWith('.html'))) {
      return `href="/epub${url}"`;
    }
    // Convert relative paths
    if (!url.startsWith('/')) {
      return `href="/epub/${url}"`;
    }
    return match;
  });
  processedHtml = processedHtml.replace(/src=["']([^"']+)["']/g, (match, url) => {
    if (url.startsWith('http') || url.startsWith('/epub/') || url.startsWith('data:')) {
      return match;
    }
    // Convert absolute paths starting with / to /epub/ (for images, css, etc.)
    if (url.startsWith('/') && (url.match(/\.(jpg|jpeg|png|gif|svg|css|js|ico)$/i))) {
      return `src="/epub${url}"`;
    }
    // Convert relative paths
    if (!url.startsWith('/')) {
      return `src="/epub/${url}"`;
    }
    return match;
  });
  // Update window.location.replace in scripts
  processedHtml = processedHtml.replace(/window\.location\.replace\(['"]([^'"]+)['"]\)/g, (match, url) => {
    if (url.startsWith('http') || url.startsWith('/')) {
      return match;
    }
    return `window.location.replace('/epub/${url}')`;
  });
  // Update meta refresh
  processedHtml = processedHtml.replace(/content=["']0; url=([^"']+)["']/g, (match, url) => {
    if (url.startsWith('http') || url.startsWith('/')) {
      return match;
    }
    return `content="0; url=/epub/${url}"`;
  });

  return (
    <>
      <Head>
        <style dangerouslySetInnerHTML={{ __html: cssContent }} />
      </Head>
      <div dangerouslySetInnerHTML={{ __html: processedHtml }} />
    </>
  );
}

export async function getServerSideProps() {
  try {
    const indexPath = path.join(process.cwd(), 'epub', 'OEBPS', 'index.html');
    const cssPath = path.join(process.cwd(), 'epub', 'OEBPS', 'styles.css');
    
    let htmlContent = '';
    let cssContent = '';
    
    if (fs.existsSync(indexPath)) {
      htmlContent = fs.readFileSync(indexPath, 'utf8');
    } else {
      console.error('index.html not found at:', indexPath);
    }
    
    if (fs.existsSync(cssPath)) {
      cssContent = fs.readFileSync(cssPath, 'utf8');
    }
    
    return {
      props: {
        htmlContent: htmlContent || '<html><body><h1>File not found</h1></body></html>',
        cssContent: cssContent || '',
      },
    };
  } catch (error) {
    console.error('Error in getServerSideProps:', error);
    return {
      props: {
        htmlContent: '<html><body><h1>Error loading index.html</h1><p>' + error.message + '</p></body></html>',
        cssContent: '',
      },
    };
  }
}

