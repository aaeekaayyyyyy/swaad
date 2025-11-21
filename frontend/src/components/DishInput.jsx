import { useState } from 'react'
import axios from 'axios'
import { API_URL } from '../config'
import './DishInput.css'

function DishInput({ onProfileCreated, initialDishes = [], onDishesUpdate }) {
  // Initialize dishes from props if provided
  const initializeDishes = () => {
    if (initialDishes && initialDishes.length > 0) {
      const categorized = {
        appetizer: [],
        mains: [],
        desserts: []
      }
      initialDishes.forEach(dish => {
        const category = dish.category || 'mains'
        categorized[category].push(dish.name || dish)
      })
      return categorized
    }
    return {
      appetizer: [],
      mains: [],
      desserts: []
    }
  }

  const [dishes, setDishes] = useState(initializeDishes())
  const [currentDish, setCurrentDish] = useState('')
  const [currentCategory, setCurrentCategory] = useState('appetizer')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [searchQuery, setSearchQuery] = useState('')

  const handleSearch = async (query) => {
    if (query.length < 2) {
      setSearchResults([])
      return
    }

    try {
      const response = await axios.get(`${API_URL}/api/search-recipes`, {
        params: { query, limit: 5 }
      })
      setSearchResults(response.data.recipes)
    } catch (err) {
      console.error('Search error:', err)
    }
  }

  const handleAddDish = (dishName) => {
    if (!dishName.trim()) return

    setDishes(prev => ({
      ...prev,
      [currentCategory]: [...prev[currentCategory], dishName.trim()]
    }))
    setCurrentDish('')
    setSearchQuery('')
    setSearchResults([])
  }

  const handleRemoveDish = (category, index) => {
    setDishes(prev => ({
      ...prev,
      [category]: prev[category].filter((_, i) => i !== index)
    }))
  }

  const handleCreateProfile = async () => {
    const allDishes = [
      ...dishes.appetizer.map(name => ({ name, category: 'appetizer' })),
      ...dishes.mains.map(name => ({ name, category: 'mains' })),
      ...dishes.desserts.map(name => ({ name, category: 'desserts' }))
    ]

    if (allDishes.length === 0) {
      setError('Please add at least one dish')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await axios.post(`${API_URL}/api/create-profile`, {
        dishes: allDishes
      })
      
      // Call onDishesUpdate if provided (for profile editing)
      if (onDishesUpdate) {
        onDishesUpdate(allDishes)
      }
      
      // Pass both profile and dishes to the callback
      onProfileCreated(response.data, allDishes)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create profile. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div className="dish-input">
      <h2>Tell us about your favorite dishes</h2>
      <p className="subtitle">Add dishes you like in each category</p>

      <div className="categories">
        {['appetizer', 'mains', 'desserts'].map(category => (
          <button
            key={category}
            className={`category-tab ${currentCategory === category ? 'active' : ''}`}
            onClick={() => setCurrentCategory(category)}
          >
            {category.charAt(0).toUpperCase() + category.slice(1)}
          </button>
        ))}
      </div>

      <div className="input-section">
        <div className="search-container">
          <input
            type="text"
            className="dish-search"
            placeholder={`Search for ${currentCategory}...`}
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value)
              handleSearch(e.target.value)
            }}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && searchQuery.trim()) {
                handleAddDish(searchQuery)
              }
            }}
          />
          {searchResults.length > 0 && (
            <div className="search-results">
              {searchResults.map((recipe, idx) => (
                <div
                  key={idx}
                  className="search-result-item"
                  onClick={() => handleAddDish(recipe.name)}
                >
                  {recipe.name}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="dish-list">
          {dishes[currentCategory].map((dish, index) => (
            <div key={index} className="dish-tag">
              <span>{dish}</span>
              <button
                className="remove-dish"
                onClick={() => handleRemoveDish(currentCategory, index)}
              >
                ×
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="all-dishes-summary">
        <h3>Your selections:</h3>
        <div className="summary">
          <div>Appetizers: {dishes.appetizer.length}</div>
          <div>Mains: {dishes.mains.length}</div>
          <div>Desserts: {dishes.desserts.length}</div>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <button
        className="create-profile-button"
        onClick={handleCreateProfile}
        disabled={loading}
      >
        {loading ? 'Creating Profile...' : 'Create My Flavor Profile'}
      </button>
    </div>
  )
}

export default DishInput

