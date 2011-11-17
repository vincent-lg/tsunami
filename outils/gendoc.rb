#!/usr/bin/env ruby

# This script exports the wiki contained in the project documentation (ID 3)

def export_text(p)
  c = p.content_for_version(nil)
  c.text
end

def export_wiki(dir, wiki)
  wiki.pages.each { |p| File.open(dir + "/" + p.title + ".txt", "w") { |f| f.write(export_text(p)) } }
  true
end

export_wiki("/home/redmine/documentation", Project.find(3).wiki)

