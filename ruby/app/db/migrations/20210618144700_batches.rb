Sequel.migration do
  change do
    create_table(:batches) do
      primary_key :id
      String :name, null: false
    end
  end
end