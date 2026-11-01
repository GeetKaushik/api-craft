const requestTabs = ["Params", "Headers", "Body", "Authorization"]

function RequestTabs({ activeTab, onSelect }) {
  return (
    <div className="editor-tabs" role="tablist" aria-label="Request settings">
      {requestTabs.map((tab) => (
        <button
          key={tab}
          role="tab"
          aria-selected={activeTab === tab}
          className={activeTab === tab ? "active" : ""}
          onClick={() => onSelect(tab)}
        >
          {tab}
        </button>
      ))}
    </div>
  )
}

export default RequestTabs
