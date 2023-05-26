# local modules (parsers)
import parser_functions.main_grouped as main_grouped
import parser_functions.main_timeseries as main_timeseries
import parser_functions.main_timeseries_audiences as main_timeseries_audiences
import parser_functions.section_1 as section1
import parser_functions.section_2_links as section2_links
import parser_functions.section_2_nodes as section2_nodes

class Parser:
  def __init__(self, creds):
    self.creds =  creds
    self.steps = {
      'EchoCh-by_state.csv': main_grouped.parse,
      'EchoCh-by_state_full-timeseries.csv': main_timeseries.parse,
      'EchoCh-TV-by_state_audiences.csv': main_timeseries_audiences.parse,
      'EchoCh-nationwide-by_gender-or-age_group.csv': section1.parse,
      'EchoCh-links.csv': section2_links.parse,
      'EchoCh-nodes.csv': section2_nodes.parse,
    }

  def parse(self, file):
    return self.steps[file["out_name"]](file)