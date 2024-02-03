# local modules (parsers)
import parser_functions.main as main
import parser_functions.section_1_grouped as section_1_grouped
import parser_functions.section_1_timeseries as section_1_timeseries
import parser_functions.section_1_timeseries_audiences as section_1_timeseries_audiences
import parser_functions.section_1_timeseries_audiences_hyperpartisan as section_1_timeseries_audiences_hyperpartisan
import parser_functions.section_2 as section2
import parser_functions.section_3_links as section3_links
import parser_functions.section_3_nodes as section3_nodes
import parser_functions.section_3_nodes_net_change_in_size as section3_nodes_net_change_in_size

class Parser:
  def __init__(self, creds):
    self.creds =  creds
    self.steps = {
      'EchoCh-national_consumption_tv_and_web.csv': main.parse,
      'EchoCh-by_state.csv': section_1_grouped.parse,
      'EchoCh-by_state_full-timeseries.csv': section_1_timeseries.parse,
      'EchoCh-by_state_audiences.csv': section_1_timeseries_audiences.parse,
      'EchoCh-by_state_audiences_hyperpartisan.csv': section_1_timeseries_audiences_hyperpartisan.parse,
      'EchoCh-nationwide-by_gender-or-age_group.csv': section2.parse,
      'EchoCh-links.csv': section3_links.parse,
      'EchoCh-nodes.csv': section3_nodes.parse,
      'EchoCh-nodes-net_change_in_size.csv': section3_nodes_net_change_in_size.parse
    }

  def parse(self, file):
    return self.steps[file["out_name"]](file)