import './Recommendations.css'

function Recommendations({ recommendations, menuDishes }) {
  const categories = ['appetizer', 'mains', 'desserts']

  const getCategoryTitle = (category) => {
    const titles = {
      appetizer: 'Appetizers',
      mains: 'Main Courses',
      desserts: 'Desserts'
    }
    return titles[category] || category
  }

  const getCategoryColor = (category) => {
    const colors = {
      appetizer: '#667eea',
      mains: '#4ade80',
      desserts: '#f59e0b'
    }
    return colors[category] || '#667eea'
  }

  return (
    <div className="recommendations">
      <h2>Recommended Dishes for You</h2>
      <p className="subtitle">Based on your flavor profile and the menu</p>

      {categories.map(category => {
        const categoryRecs = recommendations[category] || []

        return (
          <div key={category} className="recommendation-category">
            <h3 style={{ color: getCategoryColor(category) }}>
              {getCategoryTitle(category)}
            </h3>
            {categoryRecs.length === 0 ? (
              <div className="no-recommendations-category">
                <p>No recommendations found in this category from the menu.</p>
              </div>
            ) : (
              <div className="recommendation-cards">
                {categoryRecs.map((rec, idx) => (
                <div key={idx} className="recommendation-card">
                  <div className="card-header">
                    <h4>{rec.name}</h4>
                    <div className="similarity-badge" style={{ background: getCategoryColor(category) }}>
                      {(rec.similarity_score * 100).toFixed(0)}% match
                    </div>
                  </div>
                  
                  <div className="flavor-bars">
                    <div className="flavor-bar">
                      <span>Spicy</span>
                      <div className="bar-container">
                        <div 
                          className="bar-fill spicy"
                          style={{ width: `${rec.flavor_profile.spicy * 100}%` }}
                        />
                      </div>
                    </div>
                    <div className="flavor-bar">
                      <span>Sweet</span>
                      <div className="bar-container">
                        <div 
                          className="bar-fill sweet"
                          style={{ width: `${rec.flavor_profile.sweet * 100}%` }}
                        />
                      </div>
                    </div>
                    <div className="flavor-bar">
                      <span>Umami</span>
                      <div className="bar-container">
                        <div 
                          className="bar-fill umami"
                          style={{ width: `${rec.flavor_profile.umami * 100}%` }}
                        />
                      </div>
                    </div>
                    <div className="flavor-bar">
                      <span>Sour</span>
                      <div className="bar-container">
                        <div 
                          className="bar-fill sour"
                          style={{ width: `${rec.flavor_profile.sour * 100}%` }}
                        />
                      </div>
                    </div>
                    <div className="flavor-bar">
                      <span>Salty</span>
                      <div className="bar-container">
                        <div 
                          className="bar-fill salty"
                          style={{ width: `${rec.flavor_profile.salty * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  <details className="ingredients-details">
                    <summary>Ingredients</summary>
                    <div className="ingredients-list">
                      {rec.ingredients.slice(0, 10).map((ing, i) => (
                        <span key={i} className="ingredient-tag">{ing}</span>
                      ))}
                      {rec.ingredients.length > 10 && (
                        <span className="ingredient-tag">+{rec.ingredients.length - 10} more</span>
                      )}
                    </div>
                  </details>
                </div>
              ))}
              </div>
            )}
          </div>
        )
      })}

      {Object.values(recommendations).every(recs => recs.length === 0) && (
        <div className="no-recommendations">
          <p>No recommendations found. Try adding more dishes to your preferences or check the menu text.</p>
        </div>
      )}
    </div>
  )
}

export default Recommendations

