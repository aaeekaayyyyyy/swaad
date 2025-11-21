import { useState } from 'react'
import axios from 'axios'
import { API_URL } from '../config'
import './MenuUpload.css'

function MenuUpload({ onMenuProcessed, userProfile, onRecommendationsReceived }) {
  const [menuText, setMenuText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [extractedDishes, setExtractedDishes] = useState([])
  const [uploadMode, setUploadMode] = useState('text') // 'text' or 'image'
  const [selectedImage, setSelectedImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)

  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Please select an image file')
        return
      }
      setSelectedImage(file)
      setError('')
      // Create preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleProcessMenu = async () => {
    if (uploadMode === 'image') {
      if (!selectedImage) {
        setError('Please select an image to upload')
        return
      }
    } else {
      if (!menuText.trim()) {
        setError('Please enter or paste menu text')
        return
      }
    }

    setLoading(true)
    setError('')

    try {
      let dishes, categorizedDishes

      if (uploadMode === 'image') {
        // Upload image and extract text
        const formData = new FormData()
        formData.append('file', selectedImage)
        
        const extractResponse = await axios.post(`${API_URL}/api/upload-menu-image`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        dishes = extractResponse.data.dishes
        categorizedDishes = extractResponse.data.categorized || null
        // Also set the extracted text in the textarea for user to see/edit
        if (extractResponse.data.extracted_text) {
          setMenuText(extractResponse.data.extracted_text)
        }
      } else {
        // Extract dishes from menu text
        const extractResponse = await axios.post(`${API_URL}/api/process-menu`, {
          text: menuText
        })
        dishes = extractResponse.data.dishes
        categorizedDishes = extractResponse.data.categorized || null
      }

      setExtractedDishes(dishes)

      if (dishes.length === 0) {
        setError('No dishes found in the menu. Please try again with different text or image.')
        setLoading(false)
        return
      }

      // Get recommendations - pass categorized dishes if available
      const recResponse = await axios.post(`${API_URL}/api/recommendations`, {
        user_profile: userProfile,
        menu_dishes: dishes,
        categorized_dishes: categorizedDishes || null
      })

      onRecommendationsReceived(recResponse.data.recommendations)
      onMenuProcessed(dishes)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process menu. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div className="menu-upload">
      <h2>Upload or Paste Menu</h2>
      <p className="subtitle">Upload a menu image or paste menu text</p>

      {/* Mode selector */}
      <div className="upload-mode-selector">
        <button
          className={`mode-button ${uploadMode === 'text' ? 'active' : ''}`}
          onClick={() => {
            setUploadMode('text')
            setSelectedImage(null)
            setImagePreview(null)
            setError('')
          }}
        >
          📝 Text Input
        </button>
        <button
          className={`mode-button ${uploadMode === 'image' ? 'active' : ''}`}
          onClick={() => {
            setUploadMode('image')
            setMenuText('')
            setError('')
          }}
        >
          📷 Upload Image
        </button>
      </div>

      {uploadMode === 'image' ? (
        <div className="image-upload-section">
          <div className="image-upload-area">
            <input
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              id="menu-image-upload"
              style={{ display: 'none' }}
            />
            <label htmlFor="menu-image-upload" className="image-upload-label">
              {imagePreview ? (
                <div className="image-preview-container">
                  <img src={imagePreview} alt="Menu preview" className="image-preview" />
                  <div className="image-overlay">
                    <span>Click to change image</span>
                  </div>
                </div>
              ) : (
                <div className="image-upload-placeholder">
                  <div className="upload-icon">📷</div>
                  <p>Click to upload menu image</p>
                  <p className="upload-hint">Supports JPG, PNG, and other image formats</p>
                </div>
              )}
            </label>
          </div>
          {selectedImage && (
            <div className="selected-image-info">
              <p>Selected: {selectedImage.name}</p>
            </div>
          )}
        </div>
      ) : (
        <div className="menu-input-section">
          <textarea
            className="menu-textarea"
            placeholder="Paste menu text here...&#10;&#10;Example:&#10;Appetizers&#10;Caesar Salad&#10;Bruschetta&#10;&#10;Mains&#10;Grilled Salmon&#10;Pasta Carbonara&#10;&#10;Desserts&#10;Tiramisu&#10;Chocolate Cake"
            value={menuText}
            onChange={(e) => setMenuText(e.target.value)}
            rows={12}
          />
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      {extractedDishes.length > 0 && (
        <div className="extracted-dishes">
          <h3>Found {extractedDishes.length} dishes:</h3>
          <div className="dishes-list">
            {extractedDishes.slice(0, 20).map((dish, idx) => (
              <span key={idx} className="dish-badge">{dish}</span>
            ))}
            {extractedDishes.length > 20 && (
              <span className="dish-badge">+{extractedDishes.length - 20} more</span>
            )}
          </div>
        </div>
      )}

      <button
        className="process-menu-button"
        onClick={handleProcessMenu}
        disabled={loading}
      >
        {loading ? 'Processing Menu...' : 'Get Recommendations'}
      </button>

      <div className="tips">
        <h4>Tips:</h4>
        <ul>
          {uploadMode === 'image' ? (
            <>
              <li>Upload a clear photo of the menu</li>
              <li>Ensure the text is readable and well-lit</li>
              <li>The system will automatically scan and extract dish names</li>
              <li>You can edit the extracted text if needed</li>
            </>
          ) : (
            <>
              <li>Copy and paste the entire menu text</li>
              <li>Or type dish names, one per line</li>
              <li>The system will automatically extract dish names and match them to recipes</li>
            </>
          )}
        </ul>
      </div>
    </div>
  )
}

export default MenuUpload

