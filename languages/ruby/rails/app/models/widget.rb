# frozen_string_literal: true

# Example domain resource with an in-memory store. Phase-1 templates carry
# no database layer, so the store is a class-level array — replace it with
# ActiveRecord when the copied-out project needs persistence.

class Widget
  attr_reader :id, :name

  @store = []
  @next_id = 0
  @mutex = Mutex.new

  class << self
    def create(name)
      @mutex.synchronize do
        @next_id += 1
        widget = new(@next_id, name)
        @store.push(widget)
        widget
      end
    end

    def all
      @mutex.synchronize { @store.dup.sort_by(&:id) }
    end

    def find(id)
      @mutex.synchronize { @store.find { |widget| widget.id == id } }
    end

    def delete(id)
      @mutex.synchronize do
        index = @store.index { |widget| widget.id == id }
        index ? @store.delete_at(index) : nil
      end
    end
  end

  def initialize(id, name)
    @id = id
    @name = name
  end

  def as_json(*)
    { id: id, name: name }
  end
end
