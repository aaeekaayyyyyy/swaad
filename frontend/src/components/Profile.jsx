import { useState, useEffect } from 'react'
import FlavorProfile from './FlavorProfile'
import DishInput from './DishInput'
import './Profile.css'

function Profile({ userProfile, favoriteDishes, onProfileUpdate }) {
  const [flavorProfile, setFlavorProfile] = useState(userProfile)
  const [dishes, setDishes] = useState(favoriteDishes || [])
  const [editing, setEditing] = useState(false)
  const [error, setError] = useState('')

  // Update when props change
  useEffect(() => {
    if (userProfile) setFlavorProfile(userProfile)
    if (favoriteDishes) setDishes(favoriteDishes)
  }, [userProfile, favoriteDishes])

  const handleProfileUpdate = (profile, updatedDishes = []) => {
    setFlavorProfile(profile)
    setDishes(updatedDishes)
    setEditing(false)
    // Save to localStorage
    localStorage.setItem('swaad_flavor_profile', JSON.stringify(profile))
    localStorage.setItem('swaad_favorite_dishes', JSON.stringify(updatedDishes))
    // Notify parent
    if (onProfileUpdate) {
      onProfileUpdate(profile, updatedDishes)
    }
  }

  const handleDishesUpdate = (updatedDishes) => {
    setDishes(updatedDishes)
    localStorage.setItem('swaad_favorite_dishes', JSON.stringify(updatedDishes))
  }

  const handleRemoveDish = (dishName, category) => {
    const updatedDishes = dishes.filter(dish => 
      !(dish.name === dishName && dish.category === category)
    )
    setDishes(updatedDishes)
    localStorage.setItem('swaad_favorite_dishes', JSON.stringify(updatedDishes))
    // Recalculate profile if we have a callback
    if (onProfileUpdate && updatedDishes.length > 0) {
      // This will trigger a recalculation in DishInput
      setEditing(true)
    }
  }

  return (
    <div className="profile-page">
      <div className="profile-header">
        <div>
          <h1>My Flavor Profile</h1>
          <p className="user-email">Your saved preferences</p>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {!editing ? (
        <div className="profile-content">
          {flavorProfile ? (
            <>
              <div className="profile-section">
                <div className="section-header">
                  <h2>Your Flavor Profile</h2>
                  <button className="edit-button" onClick={() => setEditing(true)}>
                    Edit Profile
                  </button>
                </div>
                <FlavorProfile profile={flavorProfile} />
              </div>

              <div className="profile-section">
                <div className="section-header">
                  <h2>Your Favorite Dishes</h2>
                  <button className="edit-button" onClick={() => setEditing(true)}>
                    Edit Dishes
                  </button>
                </div>
                <div className="favorite-dishes">
                  {dishes.length > 0 ? (
                    <div className="dishes-grid">
                      {dishes.map((dish, idx) => (
                        <div key={idx} className="dish-card">
                          <span className="dish-name">{dish.name || dish}</span>
                          <span className="dish-category">{dish.category || 'mains'}</span>
                          <button
                            className="remove-dish-button"
                            onClick={() => handleRemoveDish(dish.name || dish, dish.category || 'mains')}
                          >
                            ×
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="no-dishes">No favorite dishes yet. Add some to create your profile!</p>
                  )}
                </div>
              </div>
            </>
          ) : (
            <div className="no-profile">
              <h2>Create Your Flavor Profile</h2>
              <p>Add your favorite dishes to get started!</p>
              <button className="create-profile-button" onClick={() => setEditing(true)}>
                Create Profile
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="edit-profile">
          <div className="section-header">
            <h2>Edit Your Profile</h2>
            <button className="cancel-button" onClick={() => setEditing(false)}>
              Cancel
            </button>
          </div>
          <DishInput
            onProfileCreated={handleProfileUpdate}
            initialDishes={dishes}
            onDishesUpdate={handleDishesUpdate}
          />
        </div>
      )}
    </div>
  )
}

export default Profile

