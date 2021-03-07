var express = require('express');
var router = express.Router();

const PDFToolsSdk = require('@adobe/documentservices-pdftools-node-sdk');
const credentials = PDFToolsSdk.Credentials
        .serviceAccountCredentialsBuilder()
        .fromFile("pdftools-api-credentials.json")
        .build();

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('Operations API is active.');
});

router.post('/merge', function(req, res, next) {
  console.log(req.body.file1);
  console.log(req.body.file2);
  console.log(req.body.output);
  var status = true;
  if (!req.body.file1 || !req.body.file2 || !req.body.output) {
    status=false;
  }
  else {
    try {
      // Create an ExecutionContext using credentials and create a new operation instance.
      const executionContext = PDFToolsSdk.ExecutionContext.create(credentials),
          combineFilesOperation = PDFToolsSdk.CombineFiles.Operation.createNew();
  
      // Set operation input from a source file.
      const combineSource1 = PDFToolsSdk.FileRef.createFromLocalFile(req.body.file1),
          combineSource2 = PDFToolsSdk.FileRef.createFromLocalFile(req.body.file2);
      combineFilesOperation.addInput(combineSource1);
      combineFilesOperation.addInput(combineSource2);
  
      // Execute the operation and Save the result to the specified location.
      combineFilesOperation.execute(executionContext)
          .then(result => result.saveAsFile(req.body.output))
          .catch(err => {
              if (err instanceof PDFToolsSdk.Error.ServiceApiError
                  || err instanceof PDFToolsSdk.Error.ServiceUsageError) {
                  console.log('Exception encountered while executing operation', err);
              } else {
                  console.log('Exception encountered while executing operation', err);
              }
          });
    } catch (err) {
        status = false;
        console.log('Exception encountered while executing operation', err);
    }
  }
  
  res.json({'status': status});
});

router.post('/delete', function(req, res, next) {
  console.log(req.body.output);
  console.log(req.body.file);
  console.log(req.body.page);
  var status = true;
  if (!req.body.page || !req.body.file || !req.body.output) {
    status=false;
  }
  else {
    try {
      const pageRangesForDeletion = new PDFToolsSdk.PageRanges();
      pageRangesForDeletion.addSinglePage(parseInt(req.body.page, 10));
      // Create an ExecutionContext using credentials and create a new operation instance.
      const executionContext = PDFToolsSdk.ExecutionContext.create(credentials),
          deletePagesOperation = PDFToolsSdk.DeletePages.Operation.createNew();
  
      // Set operation input from a source file.
      const input = PDFToolsSdk.FileRef.createFromLocalFile(req.body.file);
      deletePagesOperation.setInput(input);
  
      // Delete pages of the document (as specified by PageRanges).
      deletePagesOperation.setPageRanges(pageRangesForDeletion);
  
      // Execute the operation and Save the result to the specified location.
      deletePagesOperation.execute(executionContext)
          .then(result => result.saveAsFile(req.body.output))
          .catch(err => {
              if (err instanceof PDFToolsSdk.Error.ServiceApiError
                  || err instanceof PDFToolsSdk.Error.ServiceUsageError) {
                  console.log('Exception encountered while executing operation', err);
              } else {
                  console.log('Exception encountered while executing operation', err);
              }
          });
    } catch (err) {
        status = false;
        console.log('Exception encountered while executing operation', err);
    }
  }
  
  res.json({'status': status});
});

router.post('/reorder', function(req, res, next) {
  console.log(req.body.pages);
  console.log(req.body.file);
  console.log(req.body.output);
  var status = true;
  if (!req.body.pages || !req.body.file || !req.body.output) {
    status = false;
  }
  else {
    try {
      // Create an ExecutionContext using credentials and create a new operation instance.
      const executionContext = PDFToolsSdk.ExecutionContext.create(credentials),
          reorderPagesOperation = PDFToolsSdk.ReorderPages.Operation.createNew();
  
      // Set operation input from a source file, along with specifying the order of the pages for
      // rearranging the pages in a PDF file.
      const input = PDFToolsSdk.FileRef.createFromLocalFile(req.body.file);
      const pageRanges = new PDFToolsSdk.PageRanges();
      var pages = req.body.pages;
      for(let i = 0; i < pages.length; i++) {
        pageRanges.addSinglePage(parseInt(pages[i], 10));
      }
      reorderPagesOperation.setInput(input);
      reorderPagesOperation.setPagesOrder(pageRanges);
  
      // Execute the operation and Save the result to the specified location.
      reorderPagesOperation.execute(executionContext)
          .then(result => result.saveAsFile(req.body.output))
          .catch(err => {
              if(err instanceof PDFToolsSdk.Error.ServiceApiError
                  || err instanceof PDFToolsSdk.Error.ServiceUsageError) {
                  console.log('Exception encountered while executing operation', err);
              } else {
                  console.log('Exception encountered while executing operation', err);
              }
          });
    } catch (err) {
        status=false;
        console.log('Exception encountered while executing operation', err);
    }
  }

  res.json({"status": status});
});

module.exports = router;
