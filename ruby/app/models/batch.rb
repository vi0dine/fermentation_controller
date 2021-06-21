require 'sequel'

DB = Sequel.connect('sqlite://app/db/brew_valley_link.sqlite3')
class Batch < Sequel::Model
  one_to_many :steps

  def to_api
    {
      id: id,
      name: name,
      steps: steps
    }
  end
end