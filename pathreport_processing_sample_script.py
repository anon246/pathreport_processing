import pandas as pd
import os
import numpy as np
import re
import math

# Load in sample pathology report text

sample=['XXX DEPARTMENT OF PATHOLOGY XX &#x20;&#x20;SURGICAL PATHOLOGY REPORT &#x20;&#x20;&#x20;Patient Name: XXXX, XXXX Med. Rec.#: XXX DOB: XX/XX/XXXX (Age: XX) Sex: XXXXX Accession #: XXX-XXXXX Visit #: XXXXX Service Date: XX/XX/XXXX Received: XX/XX/XXXX Location: XX Client:XXX  Physician(s): XX XX &#x20;&#x20;&#x20;&#x20;FINAL PATHOLOGIC DIAGNOSIS &#x20;A.  Prostate, right apex, biopsy:  Prostatic adenocarcinoma, Gleason score 4+5=9; see comment.  &#x20;B.  Prostate, right mid, biopsy:  Prostatic adenocarcinoma, Gleason score 4+5=9, with extraprostatic extension; see comment.  &#x20;C.  Prostate, right base, biopsy:  Prostatic adenocarcinoma, Gleason score 4+4=8; see comment.  &#x20;D.  Prostate, left apex, biopsy:  Prostatic adenocarcinoma, Gleason score 5+4=9, with associated intraductal carcinoma; see comment.  &#x20;E.  Prostate, left mid, biopsy:  Prostatic adenocarcinoma, Gleason score 3+5=8, with associated intraductal carcinoma; see comment.  &#x20;F.  Prostate, left base, biopsy:  Prostatic adenocarcinoma, Gleason score 4+5=9, with associated intraductal carcinoma; see comment.  &#x20;G.  Prostate, right seminal vesicle, biopsy:  Prostatic adenocarcinoma, Gleason score 4+5=9, in seminal vesicle, with associated intraductal carcinoma; see comment.  &#x20;H.  Prostate, left seminal vesicle, biopsy:  Prostatic adenocarcinoma, Gleason score 4+5=9, in seminal vesicle, with extraprostatic extension; see comment.  &#x20;I.  Prostate, U/S right apex to mid gland, biopsy:  Prostatic adenocarcinoma, Gleason score 4+3=7 with tertiary Gleason pattern 5; see comment. &#x20;&#x20;COMMENT: The Gleason pattern 4 in this case is the expansile cribriform, fused gland, and poorly formed gland types. Gleason pattern 5 in this case is the single cell type. Perineural invasion is seen in multiple biopsies (parts A, B, C, E, F, H, and I).  In addition, many foci show features compatible with intraductal carcinoma (parts D, E, F, and G).  Extraprostatic extension into periprostatic fat is seen in part B and tumor is present in both the right (part G) and left (part H) seminal vesicles. &#x20;Specimen A  2 of 2 cores contain carcinoma. The total length of tumor in all of the cores is 35 mm. The total length of tissue in all of the cores is 36 mm. The percentage of the tissue involved by tumor is 97%. The percentage of tumor greater than Gleason pattern 3 is approximately 80%. Perineural invasion is present. No extraprostatic tumor is seen. &#x20;Specimen B  2 of 2 cores contain carcinoma. The total length of tumor in all of the cores is 33 mm. The total length of tissue in all of the cores is 37 mm. The percentage of the tissue involved by tumor is 89%. The percentage of tumor greater than Gleason pattern 3 is approximately 80%. Perineural invasion is present. Extraprostatic tumor is seen within periprostatic fat. &#x20;Specimen C  2 of 2 cores contain carcinoma. The total length of tumor in all of the cores is 27 mm. The total length of tissue in all of the cores is 35 mm. The percentage of the tissue involved by tumor is 77%. The percentage of tumor greater than Gleason pattern 3 is more than 90%. Perineural invasion is present. No definite extraprostatic tumor is seen; however a microscopic focus suspicious for extraprostatic extension is identified. &#x20;Specimen D  2 of 2 cores contain carcinoma. The total length of tumor in all of the cores is 23 mm. The total length of tissue in all of the cores is 32 mm. The percentage of the tissue involved by tumor is 72%. The percentage of tumor greater than Gleason pattern 3 is approximately 80%. Perineural invasion is not present. No extraprostatic tumor is seen. &#x20;Specimen E  2 of 2 cores contain carcinoma. The total length of tumor in all of the cores is 21 mm. The total length of tissue in all of the cores is 30 mm. The percentage of the tissue involved by tumor is 70%. The percentage of tumor greater than Gleason pattern 3 is approximately 40%. Perineural invasion is present. No definite extraprostatic tumor is seen; however a microscopic focus suspicious for extraprostatic extension is identified. &#x20;Specimen F  2 of 2 cores contain carcinoma. The total length of tumor in all of the cores is 24 mm. The total length of tissue in all of the cores is 26 mm. The percentage of the tissue involved by tumor is 92%. The percentage of tumor greater than Gleason pattern 3 approximately 80%. Perineural invasion is present. No extraprostatic tumor is seen. &#x20;Specimen G  1 of 1 core contains carcinoma. The total length of tumor in all of the cores is 16 mm. The total length of tissue in all of the cores is 16 mm. The percentage of the tissue involved by tumor is 100%. The percentage of tumor greater than Gleason pattern 3 is approximately 90%. Perineural invasion is not present. Tumor is present within the seminal vesicle.  &#x20;Specimen H  1 of 1 core contains carcinoma. The total length of tumor in all of the cores is 10 mm. The total length of tissue in all of the cores is 13 mm. The percentage of the tissue involved by tumor is 77%. The percentage of tumor greater than Gleason pattern 3 is approximately 90%. Perineural invasion is present. Tumor is present within the seminal vesicle.  &#x20;Specimen I  2 of 2 cores contain carcinoma. The total length of tumor in all of the cores is 31 mm. The total length of tissue in all of the cores is 32 mm. The percentage of the tissue involved by tumor is 97%. The percentage of tumor greater than Gleason pattern 3 is approximately 70%. Perineural invasion is present. No extraprostatic tumor is seen. &#x20;&#x20;&#x20;&#x20;Specimen(s) Received A:Right apex B:Right mid C:Right base D:Left apex E:Left mid F:Left base G:right seminal vesicle H:left seminal vesicle I:U/S right apex to mid gland &#x20;&#x20;Clinical History The patient is a 65-year-old man with elevated prostate specific antigen (XX on XX/XX/XXXX), no prior prostate biopsies, and a right apex to base lesion identified on ultrasound.  He now undergoes transrectal ultrasound-guided prostate biopsy.   &#x20;&#x20;Gross Description The case is received in 9 parts, each labeled with the patient\'s name and medical record number. &#x20;Part A is received in formalin, additionally labeled "right apex," and consists of 2 cores of tan-white tissue (2.1, 2.5 cm in length x 0.1 cm diameter). The specimen is submitted entirely in cassette A1. (XXX) &#x20;Part B is received in formalin, additionally labeled "right mid," and consists of 2 cores of tan-white tissue (1.6, 2.1 cm in length x 0.1 cm diameter). The specimen is submitted entirely in cassette B1. (XXX) &#x20;Part C is received in formalin, additionally labeled "right base," and consists of 2 cores of tan-white tissue (2, 2.2 cm in length x 0.1 cm diameter). The specimen is submitted entirely in cassette C1. (XXX) &#x20;Part D is received in formalin, additionally labeled "left apex," and consists of 2 cores of tan-white tissue (1.5, 2 cm in length x 0.1 cm diameter). The specimen is submitted entirely in cassette D1. (XXX) &#x20;Part E is received in formalin, additionally labeled "left mid," and consists of 2 cores of tan-white tissue (1.5, 2.3 cm in length x 0.1 cm diameter). The specimen is submitted entirely cassette E1. (XXX) &#x20;Part F is received in formalin, additionally labeled "left base," and consists of 2 cores of tan-white tissue (0.9, 1.7 cm in length x 0.1 cm diameter). The specimen is submitted entirely in cassette F1. (XXX) &#x20;Part G is received in formalin, additionally labeled "right seminal vesicle," and consists of a single core of tan-white tissue (1.8 cm in length x 0.1 cm diameter). The specimen is submitted entirely in cassette G1. (XXX) &#x20;Part H is received in formalin, additionally labeled "left seminal vesicle," and consists of a single core of tan-white tissue (1.6 cm in length x 0.1 cm diameter). The specimen is submitted entirely in cassette H1. (XXX) &#x20;Part I is received in formalin, additionally labeled "U/S right apex to midgland," and consists of 2 cores of tan-white tissue (1.7, 2.5 cm in length x 0.1 cm diameter). The specimen is submitted entirely in cassette I1. (XXX)  &#x20;&#x20;&#x20;Diagnosis based on gross and microscopic examinations.  Final diagnosis made by attending pathologist following review of all pathology slides.  The attending pathologist has reviewed all dictations, including prosector work, and preliminary interpretations performed by any resident involved in the case and performed all necessary edits before signing the final report. &#x20;/Pathology Resident /Pathologist      Electronically signed out on  &#x20;&#x20;&#x20;']

print('')
print('UNPROCESSED REPORT:',sample)

# Initial processing of pathology report

for report in sample:
    # check that the pathology report is related to the prostate
    if not (any(y in report for y in ['prostate', 'Prostate', 'prostatic'])):
        print('not a prostate report')
        continue
    # try to trim the report between "Diagnosis" and "Specimen"
    try:
        report_trim = report.split('Specimen')[0].split('DIAGNOSIS')[1]
    # If that doesn't work try the following strategies
    except IndexError:
        # If the report starts with "Anatomic Site", then trim report between "Final Diagnosis" and "Clinical Data".
        # Also trim report to be before "Addendum" and "Comment"
        if report.lstrip(' ').startswith('Anatomic Site'):
            try:
                report_trim = \
                    report.split('DIAGNOSIS')[1].split('CLINICAL DATA')[0].split('++++++++++Addendum.++++++++++')[
                        0].split('COMMENT')[0]
            except IndexError:
                print('misc error')
        # Specific processing for review of outside slides
        elif "Review of outside slides" in report:
            try:
                report_trim = report.split('A. ')[1]
            except IndexError:
                report_trim = report.split('1. ')[1].split('CLINICAL DATA')[0].split('++++++++++Addendum.++++++++++')[0]\
                    .split('COMMENT')[0]
        # Exclusion of Cytopath and Molecular Diagnostics reports
        elif "CYTOPATHOLOGY" in report:
            print('cytopathology error')
            continue
        elif "Molecular Diagnostics Report" in report:
            print('molecular diagnostics report error')
            continue
        # Exclusion of radiology reports and MR biopsy reports
        elif report.lstrip(' ').startswith('MR') or report.startswith('CLINICAL HISTORY') or \
                report.startswith('EXAM: MOM PROSTATE') or \
                report.startswith('OUTSIDE HOSPITAL OVERREAD MR') or \
                report.startswith('EXAM: MULTIPARAMETRIC PROSTATE') or \
                report.startswith('Prostate MRI') or \
                report.lstrip(' ').upper().startswith('OUTSIDE MR PROSTATE') or \
                ('MR PROSTATE WITH AND WITHOUT CONTRAST' in report) or \
                ('N MR PROSTATE' in report) or \
                ('MRI Prostate with and without contrast' in report) or \
                report.startswith('PMR PROSTATE') or \
                report.lstrip(' ').upper().startswith('OUTSIDE READ') or \
                ('MR PROSTATE W/SPECTROSCOPY' in report) or \
                report.startswith('CyberKnife') or \
                report.startswith('Radiology exam'):
            print('radiology report error')
            continue
        elif report.lstrip(' ').startswith('Procedure: MR'):  # MR biopsy
            print('MR biopsy error')
            continue
        else:
            print('misc error')
    except ValueError:
        print('misc error')

print('')
print('TRIMMED REPORT:',report_trim)
print('')
report_trim=[report_trim]

# Function for calculating ISUP score
def ISUP(gleason1, gleason2):
    if (gleason1 + gleason2) == 0:
        ISUPscore = 0
    elif ((gleason1 + gleason2) <= 6) & ((gleason1 + gleason2) != 0):
        ISUPscore = 1
    elif (gleason1 == 3) and (gleason2 == 4):
        ISUPscore = 2
    elif (gleason1 == 4) and (gleason2 == 3):
        ISUPscore = 3
    elif (gleason1 + gleason2) == 8:
        ISUPscore = 4
    elif (gleason1 + gleason2) == 9 or (gleason1 + gleason2) == 10:
        ISUPscore = 5
    else: ISUPscore=float('nan')
    return ISUPscore

#Function to determine highest ISUP score given list of strings (individual pathology results from report)
def sextantscore(results):
    temp=[]
    for k in range(len(results)):
        gleason = results[k].split('+')
        if len(gleason) == 2:
            try:
                temp.append(ISUP(int(gleason[0].strip(' ')[-1]),int(gleason[1].strip(' ')[0])))
            except ValueError:
                temp.append(0)
        elif len(gleason)<2:
            temp.append(0)
        elif len(gleason)>2:
            temp2=[]
            for j in list(range(1,len(gleason))):
                temp2.append(ISUP(int(gleason[j-1].strip(' ')[-1]), int(gleason[j].strip(' ')[0])))
            temp.append(np.max(temp2))
    return np.max(temp)

#Function to split pathology reports into each individual result
def path_process(report):
    #split by path result by location
    report1 = re.split('[A-Z][.] ', report.split('CLINICAL DATA')[0].split('++++++++++Addendum.++++++++++')[0].split('COMMENT')[0])
    if len(report1)==1:
        report1 = re.split('[0-9][.] ', report.split('CLINICAL DATA')[0].split('++++++++++Addendum.++++++++++')[0].split(
                                   'COMMENT')[0])
    # remove leading prostate phrase
    report2 = [x.lstrip(' ').lstrip('Prostate').lstrip(' gland').lstrip(', ').lstrip(' - ')
               for x in report1]
    return report2

sextants = ['right apex', 'right mid', 'right base', 'right anterior', 'left apex', 'left mid', 'left base',
            'left anterior']
ISUPlab = [x + '_ISUP' for x in sextants]
for report in report_trim:
    #define max score for gland
    try:
        print('Max ISUP grade in gland:',sextantscore([report]))
    except ValueError:
        print('no max gland ISUP:')
    #split by report line
    report2 = path_process(report)
    #check for MRI target results
    reportMR=[x for x in report2 if any(y in x for y in ['MR','MRI'])]
    if len(reportMR)>0:
        print('Max ISUP grade for MR target:',sextantscore(reportMR))
    else:
        print('no MR targets')
    # check for US target results
    reportUS = [x for x in report2 if any(y in x for y in ['US','U/S','ultrasound'])]
    if len(reportUS) > 0:
        print('Max ISUP grade for US target:',sextantscore(reportUS))
    else:
        print('no US targets')
    #check for systematic site biopsy results
    for loc,isup in zip(sextants,ISUPlab):
        report3 = [x for x in report2 if x.startswith(loc)]
        if len(report3) > 0:
            print(isup,sextantscore(report3))
