require 'sinatra/base'
require 'sequel'

class ApplicationController < Sinatra::Application
  register Sinatra::CrossOrigin

  before do
    @db = Sequel.connect('sqlite://brewvalley_link.db')
  end

  configure do
    enable :cross_origin

    set :allow_origin, "*"
    set :allow_methods, [:get, :post, :patch, :delete, :options]
    set :allow_credentials, true
    set :max_age, 1728000
    set :expose_headers, ['Content-Type']
  end

  options '*' do
    response.headers["Allow"] = "HEAD,GET,POST,DELETE,OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "X-Requested-With, X-HTTP-Method-Override, Content-Type, Cache-Control, Accept"
    200
  end
end