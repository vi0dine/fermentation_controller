require 'sinatra'
require 'multi_json'

require_relative '../models/batch'

class FermentationController < Sinatra::Application
  get "/batches" do
    MultiJson.dump(Batch.association_join(:steps).all.map(&:to_api))
  end
end