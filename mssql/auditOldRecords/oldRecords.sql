SELECT p.presId,p.presProfile_profId,p.presPresenterName,p.presTitle,p.presStartTime,f.filePresentation_presId,f.fileId,f.fileJob_jobId,f.fileName,f.filePath,f.fileCreationTime
  FROM [Relay510].[transferService].[tblPresentation] p
  JOIN [Relay510].[transferService].[tblFile] f ON f.filePresentation_presId = p.presId
  WHERE presProfile_profId IN (39,43)
  AND p.presRecordTime < DATEADD(MONTH,-4,GETDATE())
  ORDER BY presProfile_profId ASC
