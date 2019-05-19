defmodule ForgeAbi.GeneralTicket do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          id: String.t(),
          start_time: String.t(),
          end_time: String.t(),
          location: String.t(),
          img_url: String.t(),
          title: String.t()
        }
  defstruct [:id, :start_time, :end_time, :location, :img_url, :title]

  field :id, 1, type: :string
  field :start_time, 2, type: :string
  field :end_time, 3, type: :string
  field :location, 4, type: :string
  field :img_url, 6, type: :string
  field :title, 7, type: :string
end

defmodule ForgeAbi.EventInfo do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          details: String.t(),
          consume_asset_tx: binary
        }
  defstruct [:details, :consume_asset_tx]

  field :details, 1, type: :string
  field :consume_asset_tx, 2, type: :bytes
end
