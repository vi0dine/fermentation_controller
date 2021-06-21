require 'sequel'

DB = Sequel.connect('sqlite://app/db/brew_valley_link.sqlite3')
class Step < Sequel::Model
  many_to_one :batch
end