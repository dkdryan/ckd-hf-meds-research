## LIBRARIES

# cohort extractor
from cohortextractor import (StudyDefinition, patients, codelist_from_csv, codelist)

##CODE LIST
systolic_blood_pressure_codes = codelist(["2469."], system="ctv3")
ace_inhibitor_codes = codelist_from_csv("codelists/opensafely-ace-inhibitor-medications.csv",system="snomed",column="id")
arb_inhibitor_codes = codelist_from_csv("codelists/opensafely-angiotensin-ii-receptor-blockers-arbs.csv", system='snomed', column='id')
hf_codes = codelist_from_csv("codelists/opensafely-heart-failure.csv", system="ctv3", column="CTV3ID")
ckd_codes = codelist_from_csv("codelists/opensafely-chronic-kidney-disease.csv", system="ctv3", column="CTV3ID")

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
    population = patients.all(),

    # define the study variables

    age = patients.age_as_of("2020-02-01",
                             return_expectations={"rate" : "universal", "int" : {"distribution" : "population_ages"}}),
   
    ## bmi
   
    bmi=patients.most_recent_bmi(between=["2010-02-01", "2020-01-31"],
                                 minimum_age_at_measurement=18, include_measurement_date=True, date_format="YYYY-MM",
                                 return_expectations={"date": {"earliest": "2010-02-01", "latest": "2020-01-31"},
                                                      "float": {"distribution": "normal", "mean": 28, "stddev": 8},
                                                      "incidence": 0.80,}),
   
    ## systolic blood pressure
   
    bp_sys=patients.mean_recorded_value(systolic_blood_pressure_codes,
                                        on_most_recent_day_of_measurement=True,
                                        between=["2017-02-01", "2020-01-31"],
                                        include_measurement_date=True,
                                        date_format="YYYY-MM",
                                        return_expectations={"float": {"distribution": "normal", "mean": 80, "stddev": 10},
                                                             "date": {"earliest": "2019-02-01", "latest": "2020-01-31"},
                                                             "incidence": 0.95,}),
   
    ## ace inhibitor
   
    ace_inhibitor = patients.with_these_medications(ace_inhibitor_codes,
                                                   between=["1900-01-01", "2020-02-01"],
                                                   include_date_of_match = True,
                                                   date_format="YYYY-MM-DD",
                                                   returning="binary_flag",
                                                   return_expectations = {"incidence": 0.05,
                                                                         "date": {"earliest": "1980-02-01",
                                                                                  "latest": "2020-01-31"}}),

    ## arb
   
     arb_inhibitor = patients.with_these_medications(arb_inhibitor_codes,
                                                   between=["1900-01-01", "2020-02-01"],
                                                   include_date_of_match = True,
                                                   date_format="YYYY-MM-DD",
                                                   returning="binary_flag",
                                                   return_expectations = {"incidence": 0.05,
                                                                         "date": {"earliest": "1980-02-01",
                                                                                  "latest": "2020-01-31"}}),
   
    ## ckd
   
    ckd = patients.with_these_clinical_events(ckd_codes,
                                              return_first_date_in_period=True,
                                              include_month=True),
   
    ## hf
   
    hf = patients.with_these_clinical_events(hf_codes,
                                             return_first_date_in_period=True,
                                             include_month=True))