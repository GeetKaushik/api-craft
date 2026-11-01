import { Import, TerminalSquare, X } from "lucide-react"

const modalContent = {
  collection: {
    title: "New collection",
    description: "Collection creation is not implemented yet. No data will be saved.",
  },
  import: {
    title: "Import a collection",
    description: "Import is not implemented yet. No files or external services will be accessed.",
  },
}

function Modal({ type, onClose }) {
  const content = modalContent[type]
  if (!content) return null

  return (
    <div className="dialog-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose() }}>
      <section className="placeholder-dialog" role="dialog" aria-modal="true" aria-labelledby="dialog-title">
        <button className="icon-button dialog-close" aria-label="Close dialog" onClick={onClose}><X size={17} /></button>
        <span className="dialog-icon"><TerminalSquare size={19} /></span>
        <h2 id="dialog-title">{content.title}</h2>
        <p>{content.description}</p>
        {type === "import" && <div className="import-preview"><Import size={16} /> OpenAPI / Postman <span>Not implemented</span></div>}
        <div className="dialog-actions">
          <button className="secondary-button" onClick={onClose}>Close</button>
        </div>
      </section>
    </div>
  )
}

export default Modal
