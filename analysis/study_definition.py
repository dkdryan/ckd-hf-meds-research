## cohort extractor
from cohortextractor import (StudyDefinition, patients, codelist_from_csv, codelist)

## codes - imported from codelist 
ethnicity_codes = codelist_from_csv("codelists/opensafely-ethnicity.csv",
                                        system="ctv3",
                                        column="Code",
                                        category_column="Grouping_6")

diabetes_codes = codelist_from_csv("codelists/opensafely-diabetes.csv", system="ctv3", column="CTV3ID")
hf_codes = codelist_from_csv("codelists/opensafely-heart-failure.csv", system="ctv3", column="CTV3ID")
ckd_codes = codelist_from_csv("codelists/opensafely-chronic-kidney-disease.csv", system="ctv3", column="CTV3ID")
dialysis_codes = codelist_from_csv("codelists/opensafely-dialysis.csv", system="ctv3", column="CTV3ID")
ace_codes = codelist_from_csv("codelists/opensafely-ace-inhibitor-medications.csv",system="snomed",column="id")
arb_codes = codelist_from_csv("codelists/opensafely-angiotensin-ii-receptor-blockers-arbs.csv", system='snomed', column='id')
bb_codes = codelist_from_csv("codelists/opensafely-beta-blocker-medications.csv", system="snomed", column="id")
thiazide_codes = codelist_from_csv("codelists/opensafely-thiazide-type-diuretic-medication.csv", system="snomed", column="id")

## codes - already within the opensafely system 
creatinine_codes = codelist(["XE2q5"], system="ctv3")
hba1c_new_codes = codelist(["XaPbt", "Xaeze", "Xaezd"], system="ctv3")
hba1c_old_codes = codelist(["X772q", "XaERo", "XaERp"], system="ctv3")
systolic_blood_pressure_codes = codelist(["2469."], system="ctv3")

## STUDY POPULATION
study = StudyDefinition(

    # define default dummy data behaviour
    # Configure the expectations framework
    default_expectations = {
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "exponential_increase",
        "incidence": 0.5,
        "float": {"distribution": "normal", "mean": 80, "stddev": 10}},
 
   
    # define the study index date
    index_date = "2020-01-01",

    # define the study population
    population = patients.with_these_clinical_events(hf_codes, on_or_after = "2000-01-01"),

    # define the study variables

    age = patients.age_as_of("2020-12-16",
                             return_expectations={"rate" : "universal", "int" : {"distribution" : "population_ages"}}),
   
    ## bmi
   
    bmi=patients.most_recent_bmi(between=["2010-01-01", "2020-12-16"],
                                 minimum_age_at_measurement=18, include_measurement_date=True, date_format="YYYY-MM",
                                 return_expectations={"date": {"earliest": "2010-02-01", "latest": "2020-01-31"},
                                                      "float": {"distribution": "normal", "mean": 28, "stddev": 8},
                                                      "incidence": 0.80,}),
   
    ## systolic blood pressure
   
    bp_sys=patients.mean_recorded_value(systolic_blood_pressure_codes,
                                        on_most_recent_day_of_measurement=True,
                                        between=["2017-01-01", "2020-12-16"],
                                        include_measurement_date=True,
                                        date_format="YYYY-MM",
                                        return_expectations={"float": {"distribution": "normal", "mean": 80, "stddev": 10},
                                                             "date": {"earliest": "2019-02-01", "latest": "2020-01-31"},
                                                             "incidence": 0.95,}),
   
    ## ace inhibitor
   
    ace_inhibitor = patients.with_these_medications(ace_codes,
                                                   between=["2000-01-01", "2020-12-16"],
                                                   include_date_of_match = True,
                                                   date_format="YYYY-MM-DD",
                                                   returning="binary_flag",
                                                   return_expectations = {"incidence": 0.05,
                                                                         "date": {"earliest": "2000-01-01",
                                                                                  "latest": "2020-12-16"}}),

    ## arb
   
     arb_inhibitor = patients.with_these_medications(arb_codes,
                                                   between=["2000-01-01", "2020-12-16"],
                                                   include_date_of_match = True,
                                                   date_format="YYYY-MM-DD",
                                                   returning="binary_flag",
                                                   return_expectations = {"incidence": 0.05,
                                                                         "date": {"earliest": "2000-01-01",
                                                                                  "latest": "2020-12-16"}}),
   
    ## ckd
   
    ckd = patients.with_these_clinical_events(ckd_codes,
                                              return_first_date_in_period=True,
                                              include_month=True),
    
    ## dialysis 
    
    dialysis = patients.with_these_clinical_events(dialysis_codes, 
                                                   return_first_date_in_period=True, 
                                                   include_month=True), 

    ## ethnicity 
    
    ethnicity_codes = patients.with_these_clinical_events(ethnicity_codes, 
                                                          returning="category", 
                                                          find_last_match_in_period=True, 
                                                          include_date_of_match=False, 
                                                          return_expectations={"category": 
                                                                                  {"ratios": 
                                                                                   {"1": 0.6, 
                                                                                    "2": 0.2,
                                                                                    "3": 0.025, 
                                                                                    "4": 0.025, 
                                                                                    "5": 0.15}}}),
    
    ## blood tests 
    
    creatinine = patients.with_these_clinical_events(creatinine_codes, 
                                                   find_last_match_in_period=True,
                                                   on_or_before="2020-12-16",
                                                   returning="numeric_value",
                                                   include_date_of_match=True,
                                                   include_month=True,
                                                   return_expectations={
                                                       "float": {"distribution": "normal", "mean": 80, "stddev": 10},
                                                       "date": {"earliest": "2019-02-01", "latest": "2020-01-31"},
                                                       "incidence": 0.95}),
    
    hba1c_new = patients.with_these_clinical_events(hba1c_new_codes, 
                                                   find_last_match_in_period=True,
                                                   on_or_before="2020-12-16",
                                                   returning="numeric_value",
                                                   include_date_of_match=True,
                                                   include_month=True,
                                                   return_expectations={
                                                       "float": {"distribution": "normal", "mean": 80, "stddev": 10},
                                                       "date": {"earliest": "2019-02-01", "latest": "2020-01-31"},
                                                       "incidence": 0.95}),
    
    
    hba1c_old = patients.with_these_clinical_events(hba1c_old_codes, 
                                                   find_last_match_in_period=True,
                                                   on_or_before="2020-12-16",
                                                   returning="numeric_value",
                                                   include_date_of_match=True,
                                                   include_month=True, 
                                                   return_expectations={
                                                       "float": {"distribution": "normal", "mean": 80, "stddev": 10},
                                                       "date": {"earliest": "2019-02-01", "latest": "2020-01-31"},
                                                       "incidence": 0.95}))
    
    
    
    