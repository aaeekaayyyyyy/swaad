import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend } from 'recharts'
import './FlavorProfile.css'

function FlavorProfile({ profile }) {
  const prepareData = (category, profileData) => {
    return [
      { flavor: 'Spicy', value: profileData.spicy * 100 },
      { flavor: 'Sweet', value: profileData.sweet * 100 },
      { flavor: 'Umami', value: profileData.umami * 100 },
      { flavor: 'Sour', value: profileData.sour * 100 },
      { flavor: 'Salty', value: profileData.salty * 100 }
    ]
  }

  const appetizerData = prepareData('appetizer', profile.appetizer)
  const mainsData = prepareData('mains', profile.mains)
  const dessertsData = prepareData('desserts', profile.desserts)

  const allData = appetizerData.map((item, index) => ({
    flavor: item.flavor,
    appetizer: item.value,
    mains: mainsData[index].value,
    desserts: dessertsData[index].value
  }))

  return (
    <div className="flavor-profile">
      <h2>Your Flavor Profile</h2>
      <p className="subtitle">Based on your favorite dishes</p>

      <div className="profile-charts">
        <div className="chart-container">
          <h3>Appetizers</h3>
          <RadarChart width={300} height={300} data={appetizerData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="flavor" />
            <PolarRadiusAxis angle={90} domain={[0, 100]} />
            <Radar
              name="Appetizer"
              dataKey="value"
              stroke="#667eea"
              fill="#667eea"
              fillOpacity={0.6}
            />
          </RadarChart>
          <div className="profile-values">
            {Object.entries(profile.appetizer).map(([key, value]) => (
              <div key={key} className="value-item">
                <span className="value-label">{key}:</span>
                <span className="value-number">{(value * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </div>

        <div className="chart-container">
          <h3>Mains</h3>
          <RadarChart width={300} height={300} data={mainsData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="flavor" />
            <PolarRadiusAxis angle={90} domain={[0, 100]} />
            <Radar
              name="Mains"
              dataKey="value"
              stroke="#4ade80"
              fill="#4ade80"
              fillOpacity={0.6}
            />
          </RadarChart>
          <div className="profile-values">
            {Object.entries(profile.mains).map(([key, value]) => (
              <div key={key} className="value-item">
                <span className="value-label">{key}:</span>
                <span className="value-number">{(value * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </div>

        <div className="chart-container">
          <h3>Desserts</h3>
          <RadarChart width={300} height={300} data={dessertsData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="flavor" />
            <PolarRadiusAxis angle={90} domain={[0, 100]} />
            <Radar
              name="Desserts"
              dataKey="value"
              stroke="#f59e0b"
              fill="#f59e0b"
              fillOpacity={0.6}
            />
          </RadarChart>
          <div className="profile-values">
            {Object.entries(profile.desserts).map(([key, value]) => (
              <div key={key} className="value-item">
                <span className="value-label">{key}:</span>
                <span className="value-number">{(value * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default FlavorProfile

