import { useState } from "react"
import { Braces, ChevronDown, Command, Layers3, Search, Settings2 } from "lucide-react"

function AppHeader({ onNotice }) {
  const [search, setSearch] = useState("")

  return (
    <header className="app-header">
      <a className="brand" href="#overview" aria-label="API Craft home">
        <span className="brand-mark"><Braces size={19} strokeWidth={2.5} /></span>
        <span className="brand-name">API<span>Craft</span></span>
      </a>
      <div className="header-divider" />
      <div className="workspace-picker" aria-label="Workspace">
        <span className="workspace-avatar"><Layers3 size={15} /></span>
        <span className="workspace-label"><strong>No workspace selected</strong><small>Workspace unavailable</small></span>
        <ChevronDown size={15} />
      </div>
      <label className="command-search">
        <Search size={16} />
        <input
          aria-label="Search requests and collections"
          placeholder="Search requests, collections..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <span className="shortcut"><Command size={11} /> K</span>
      </label>
      <div className="header-actions">
        <label className="environment-picker">
          <select aria-label="Environment" disabled defaultValue="">
            <option value="">No environments available</option>
          </select>
          <ChevronDown size={14} />
        </label>
        <button className="icon-button" aria-label="Open settings" onClick={() => onNotice("Not implemented yet.")}>
          <Settings2 size={17} />
        </button>
      </div>
    </header>
  )
}

export default AppHeader
