# modules
from os import getenv
  
# local modules
from parsers import Parser

# global vars
AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
bucket = getenv('bucket')

# # datasets
datasets = [
  {
    'url': [
      'raw_data/all_adults_national_tv_consumption_f1.csv',
      'raw_data/by_age_national_tv_consumption_f1.csv',
      'raw_data/by_age_x_gender_national_tv_consumption_f1.csv',
      'raw_data/by_gender_national_tv_consumption_f1.csv',
      'raw_data/by_state_national_tv_consumption_f1.csv',
      'raw_data/all_adults_desktop_web_consumption_f1.csv',
      'raw_data/by_gender_desktop_web_consumption_f1.csv',
      'raw_data/by_age_desktop_web_consumption_f1.csv',
      'raw_data/by_age_x_gender_desktop_web_consumption_f1.csv',
      'raw_data/by_state_desktop_web_consumption_f1.csv',
    ],
    'out_name': 'EchoCh-national_consumption_tv_and_web.csv',
    'format': '%.3f'
  },
  {
    'url': [
      'raw_data/TVLeftEchoChLenient_by_state.csv',
      'raw_data/TVLeftEchoChStringent_by_state.csv',
      'raw_data/TVRightEchoChLenient_by_state.csv',
      'raw_data/web_ec_sizes_by_state.csv',
      ], 
    'out_name': 'EchoCh-by_state.csv',
    'format': '%.4f'
  },
  {
    'url': [
      'raw_data/TVLeftEchoChLenient_by_state.csv',
      'raw_data/TVLeftEchoChStringent_by_state.csv',
      'raw_data/TVRightEchoChLenient_by_state.csv',
      'raw_data/web_ec_sizes_by_state.csv',
      ], 
    'out_name': 'EchoCh-by_state_full-timeseries.csv',
    'format': '%.3f'
  },
  {
    'url': [
      'raw_data/news_domains_ranked_by_audiences_agg=last_3_months_dem=state_top_programs.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=last_6_months_dem=state_top_programs.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=last_12_months_dem=state_top_programs.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=since 2016_dem=state_top_programs.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=last_3_months_dem=state_top_domains.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=last_6_months_dem=state_top_domains.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=last_12_months_dem=state_top_domains.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=since 2016_dem=state_top_domains.csv',
    ],
    'out_name': 'EchoCh-by_state_audiences.csv',
    'format': '%.0f'
  },
  {
    'url': [
      'raw_data/news_domains_ranked_by_audiences_agg=last_3_months_dem=state_top_programs.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=last_6_months_dem=state_top_programs.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=last_12_months_dem=state_top_programs.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=since 2016_dem=state_top_programs.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=last_3_months_dem=state_top_domains.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=last_6_months_dem=state_top_domains.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=last_12_months_dem=state_top_domains.csv',
      'raw_data/news_domains_ranked_by_audiences_agg=since 2016_dem=state_top_domains.csv',
    ],
    'out_name': 'EchoCh-by_state_audiences_hyperpartisan.csv',
    'format': '%.0f'
  },
  {
    'url': [
      'raw_data/TVLeftEchoChLenient_all_adults.csv',
      'raw_data/TVLeftEchoChLenient_by_age_x_gender.csv',
      'raw_data/TVLeftEchoChLenient_by_age.csv',
      'raw_data/TVLeftEchoChLenient_by_gender.csv',
      'raw_data/TVLeftEchoChStringent_all_adults.csv',
      'raw_data/TVLeftEchoChStringent_by_age_x_gender.csv',
      'raw_data/TVLeftEchoChStringent_by_age.csv',
      'raw_data/TVLeftEchoChStringent_by_gender.csv',
      'raw_data/TVRightEchoChLenient_all_adults.csv',
      'raw_data/TVRightEchoChLenient_by_age_x_gender.csv',
      'raw_data/TVRightEchoChLenient_by_age.csv',
      'raw_data/TVRightEchoChLenient_by_gender.csv',
      'raw_data/web_ec_sizes_all_adults.csv',
      'raw_data/web_ec_sizes_by_age_x_gender.csv',
      'raw_data/web_ec_sizes_by_age.csv',
      'raw_data/web_ec_sizes_by_gender.csv',
      ], 
    'out_name': 'EchoCh-nationwide-by_gender-or-age_group.csv',
    'format': '%.3f'
  },
  {
    'url': 'raw_data/tv_archetype_flow_data.csv',
    'out_name': 'EchoCh-links.csv',
    'format': '%.3f'
  },
  {
  'url': [
    'raw_data/tv_archetype_sizes.csv',
    'raw_data/tv_archetype_mins_p_person.csv'
    ],
  'out_name': 'EchoCh-nodes.csv',
  'format': '%.5f'
  },
]
# credentials
creds = {
  "key": AWS_ACCESS_KEY_ID,
  "secret": AWS_SECRET_ACCESS_KEY
}
# instantiate parser
file_parser = Parser(creds)

# # iterate over files that need parsing 
for file in datasets:
  out_data = file_parser.parse(file)

  # # save data to different location
  out_data.to_csv(
    # f's3://{bucket}/processed/{file["out_name"]}',
    f'../processed_data/{file["out_name"]}',
    index=False,
    float_format=file["format"]
  )
