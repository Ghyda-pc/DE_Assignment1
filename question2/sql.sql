create table loan_data_set(
    Loan_ID   text,
    Gender    text,
    Married   text,
    ApplicantIncome int,
    Loan_Status text );

COPY loan_data_set(Loan_ID, Gender, Married, ApplicantIncome, Loan_Status)
    FROM '/file.csv'
    DELIMITER ','
    CSV HEADER;