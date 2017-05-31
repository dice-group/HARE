#!/bin/bash

#Downloads
#  wget http://downloads.dbpedia.org/2016-04/core-i18n/en/disambiguations_en.ttl.bz2
#  bunzip2 disambiguations_en.ttl.bz2
  wget http://downloads.dbpedia.org/2016-04/core-i18n/en/instance_types_en.ttl.bz2
  bunzip2 instance_types_en.ttl.bz2
#  wget http://downloads.dbpedia.org/2016-04/core-i18n/en/long_abstracts_en.ttl.bz2
#  bunzip2 long_abstracts_en.ttl.bz2
  wget http://downloads.dbpedia.org/2016-04/core-i18n/en/pnd_en.ttl.bz2
  bunzip2 pnd_en.ttl.bz2
#  wget http://downloads.dbpedia.org/2016-04/core-i18n/en/labels_en.ttl.bz2
#  bunzip2 labels_en.ttl.bz2
  wget http://downloads.dbpedia.org/2016-04/core-i18n/en/mappingbased_literals_en.ttl.bz2
  bunzip2 mappingbased_literals_en.ttl.bz2
  wget http://downloads.dbpedia.org/2016-04/core-i18n/en/mappingbased_objects_en.ttl.bz2
  bunzip2 mappingbased_objects_en.ttl.bz2
  wget http://downloads.dbpedia.org/2016-04/core-i18n/en/persondata_en.ttl.bz2
  bunzip2 persondata_en.ttl.bz2
  wget http://downloads.dbpedia.org/2016-04/core-i18n/en/specific_mappingbased_properties_en.ttl.bz2
  bunzip2 specific_mappingbased_properties_en.ttl.bz2
#  wget http://downloads.dbpedia.org/2016-04/core-i18n/en/transitive_redirects_en.ttl.bz2
#  bunzip2 transitive_redirects_en.ttl.bz2


#concatenate
cat *.ttl > dbpedia.ttl


#Clean up

rm mappingbased_literals_en.ttl transitive_redirects_en.ttl. mappingbased_objects_en.ttl labels_en.ttl specific_mappingbased_properties_en.ttl disambiguations_en.ttl labels_en.ttl persondata_en.ttl en_surface_forms.ttl instance_types_en.ttl  pnd_en.ttl transitive_redirects_en.ttl
