Sequel.migration do
  change do
    create_table(:steps) do
      primary_key :id
      Float :temperature, null: false
      Integer :time, null: false
      foreign_key :batch_id, :batches
    end
  end
end