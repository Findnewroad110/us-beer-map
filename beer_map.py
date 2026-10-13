import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Page Configuration (UI text changed to English)
st.set_page_config(page_title="US 50 States Craft Beer Map", layout="wide")
st.title("🗺️ US 50 States Craft Beer Explorer")
st.markdown("Discover the Top 3 breweries and their signature beers across all 50 states! Hover over the map or check the database below.")

# 2. Massive 50-State CSV Data (150 Breweries, 300 Beers with Types)
csv_data = """State,City,Lat,Lon,Brewery,Beer1,Beer2
Alabama,Birmingham,33.52,-86.81,Good People Brewing,Snake Handler (Double IPA),Muchacho (Mexican Lager)
Alabama,Birmingham,33.51,-86.80,TrimTab Brewing,TrimTab IPA (IPA),Paradise Now (Berliner Weisse)
Alabama,Huntsville,34.73,-86.58,Straight to Ale,Monkeynaut (IPA),Lily Flagg (Milk Stout)
Alaska,Juneau,58.30,-134.41,Alaskan Brewing Co.,Alaskan Amber (Altbier),Smoked Porter (Porter)
Alaska,Anchorage,61.21,-149.90,Anchorage Brewing Co.,Galaxy White IPA (White IPA),A Deal With The Devil (Barleywine)
Alaska,Anchorage,61.16,-149.87,Midnight Sun Brewing,Panty Peeler (Tripel),Kodiak Brown (Brown Ale)
Arizona,Phoenix,33.44,-112.07,Wren House Brewing,Spellbinder (Hazy IPA),Jomax (Oatmeal Stout)
Arizona,Gilbert,33.35,-111.78,Arizona Wilderness,Refuge (IPA),Pecan Pie Brown (Brown Ale)
Arizona,Tempe,33.42,-111.94,Four Peaks Brewing,Kilt Lifter (Scottish Ale),Hop Knot (IPA)
Arkansas,Rogers,36.33,-94.11,Ozark Beer Co.,Ozark IPA (IPA),Cream Stout (Milk Stout)
Arkansas,Little Rock,34.74,-92.28,Lost Forty Brewing,Love Honey (Bock),Day Drinker (Belgian Blonde)
Arkansas,Little Rock,34.75,-92.27,Flyway Brewing,Bluewing (Blueberry Wheat),Early Bird (IPA)
California,Santa Rosa,38.44,-122.71,Russian River Brewing,Pliny the Elder (Double IPA),Blind Pig (IPA)
California,Chico,39.72,-121.81,Sierra Nevada Brewing,Pale Ale (Pale Ale),Torpedo (Extra IPA)
California,San Diego,32.71,-117.16,Stone Brewing,Stone IPA (IPA),Arrogant Bastard (Strong Ale)
Colorado,Denver,39.73,-104.99,Great Divide Brewing,Yeti (Imperial Stout),Titan (IPA)
Colorado,Fort Collins,40.58,-105.08,New Belgium Brewing,Fat Tire (Amber Ale),Voodoo Ranger (IPA)
Colorado,Longmont,40.16,-105.10,Left Hand Brewing,Milk Stout Nitro (Sweet Stout),Sawtooth (Amber Ale)
Connecticut,Stratford,41.18,-73.13,Two Roads Brewing,Road 2 Ruin (Double IPA),Two Juicy (Hazy IPA)
Connecticut,Woodbridge,41.35,-73.01,New England Brewing,Sea Hag (IPA),Fuzzy Baby Ducks (IPA)
Connecticut,Salem,41.48,-72.27,Fox Farm Brewery,Gather (Pilsner),Burst (IPA)
Delaware,Milton,38.77,-75.31,Dogfish Head Brewery,90 Minute IPA (Double IPA),SeaQuench Ale (Sour)
Delaware,Newark,39.68,-75.74,Iron Hill Brewery,Philly Phavorite (Hazy IPA),Pig Iron (Porter)
Delaware,Dewey Beach,38.69,-75.07,Dewey Beer Co.,Secret Machine (Fruited Sour),Swishy Pants (IPA)
Florida,Tampa,27.95,-82.45,Cigar City Brewing,Jai Alai (IPA),Maduro (Brown Ale)
Florida,Miami,25.80,-80.19,J. Wakefield Brewing,DFPF (Berliner Weisse),El Jefe (Hefeweizen)
Florida,Oakland Park,26.17,-80.13,Funky Buddha Brewery,Maple Bacon Coffee (Porter),Floridian (Hefeweizen)
Georgia,Athens,33.95,-83.37,Creature Comforts,Tropicália (IPA),Athena (Berliner Weisse)
Georgia,Atlanta,33.74,-84.38,SweetWater Brewing,420 Extra Pale Ale (Pale Ale),Goin' Coastal (IPA)
Georgia,Atlanta,33.75,-84.39,Monday Night Brewing,Slap Fight (IPA),Drafty Kilt (Scotch Ale)
Hawaii,Kihei,20.76,-156.45,Maui Brewing Co.,Bikini Blonde (Lager),Coconut Hiwa (Porter)
Hawaii,Kailua-Kona,19.64,-155.99,Kona Brewing Co.,Big Wave (Golden Ale),Longboard (Island Lager)
Hawaii,Honolulu,21.30,-157.85,Honolulu BeerWorks,Kewalos (Cream Ale),Hop Island (IPA)
Idaho,Victor,43.60,-111.11,Grand Teton Brewing,Sweetgrass (American Pale Ale),Bitch Creek (Brown Ale)
Idaho,Boise,43.61,-116.20,Payette Brewing Co.,Rustler (IPA),North Fork (Lager)
Idaho,Nampa,43.58,-116.56,Mother Earth Brew Co.,Cali Creamin' (Cream Ale),Boo Koo (IPA)
Illinois,Chicago,41.93,-87.70,Revolution Brewing,Anti-Hero (IPA),Eugene (Porter)
Illinois,Chicago,41.95,-87.67,Half Acre Beer Co.,Daisy Cutter (Pale Ale),Bodem (IPA)
Illinois,Chicago,41.88,-87.67,Goose Island Beer Co.,Bourbon County (Stout),312 Urban (Wheat Ale)
Indiana,Munster,41.56,-87.50,3 Floyds Brewing,Zombie Dust (Pale Ale),Gumballhead (Wheat Beer)
Indiana,Indianapolis,39.76,-86.15,Sun King Brewery,Sunlight (Cream Ale),Wee Mac (Scottish Ale)
Indiana,Bloomington,39.16,-86.53,Upland Brewing Co.,Dragonfly (IPA),Wheat (Belgian Witbier)
Iowa,Decorah,43.30,-91.78,Toppling Goliath,Pseudo Sue (Pale Ale),King Sue (Double IPA)
Iowa,Des Moines,41.58,-93.62,Lua Brewing,Push Pop (Fruited Sour),High Fives (IPA)
Iowa,Iowa City,41.66,-91.53,Big Grove Brewery,Easy Eddy (Hazy IPA),Arms Race (Pale Ale)
Kansas,Lawrence,38.97,-95.23,Free State Brewing,Ad Astra Ale (Altbier),Copperhead (Pale Ale)
Kansas,Wichita,37.68,-97.33,Wichita Brewing Co.,V.V. (IPA),Valleyview (Vanilla Porter)
Kansas,Lenexa,38.96,-94.72,Limitless Brewing,JOCO (Hazy IPA),Ryes and Shine (Rye Beer)
Kentucky,Louisville,38.25,-85.74,Against the Grain,The Brown Note (Brown Ale),Citra Ass Down (Double IPA)
Kentucky,Lexington,38.04,-84.50,West Sixth Brewing,West Sixth IPA (IPA),Pay It Forward (Brown Ale)
Kentucky,Lexington,38.05,-84.51,Country Boy Brewing,Cougar Bait (Blonde Ale),Shotgun Wedding (Brown Ale)
Louisiana,Abita Springs,30.47,-89.96,Abita Brewing Co.,Purple Haze (Raspberry Wheat),Andygator (Doppelbock)
Louisiana,Broussard,30.14,-91.96,Parish Brewing Co.,Ghost In The Machine (Double IPA),Canebrake (Wheat Ale)
Louisiana,New Orleans,29.95,-90.07,NOLA Brewing,NOLA Blonde (Blonde Ale),Irish Channel (Stout)
Maine,Portland,43.66,-70.25,Allagash Brewing Co.,Allagash White (Witbier),Curieux (Tripel)
Maine,Freeport,43.85,-70.10,Maine Beer Co.,Lunch (IPA),Dinner (Double IPA)
Maine,Portland,43.65,-70.26,Bissell Brothers,The Substance (IPA),Swish (Double IPA)
Maryland,Frederick,39.41,-77.41,Flying Dog Brewery,Raging Bitch (Belgian IPA),Bloodline (Blood Orange Ale)
Maryland,Baltimore,39.29,-76.61,Heavy Seas Beer,Loose Cannon (IPA),Peg Leg (Imperial Stout)
Maryland,Baltimore,39.30,-76.62,Union Craft Brewing,Duckpin (Pale Ale),Divine (IPA)
Massachusetts,Charlton,42.13,-72.00,Tree House Brewing,Julius (IPA),Green (IPA)
Massachusetts,Canton,42.15,-71.14,Trillium Brewing,Congress Street (IPA),Fort Point (Pale Ale)
Massachusetts,Boston,42.31,-71.10,Samuel Adams,Boston Lager (Lager),Wicked Hazy (Hazy IPA)
Michigan,Kalamazoo,42.29,-85.58,Bell's Brewery,Two Hearted Ale (IPA),Oberon (Wheat Ale)
Michigan,Grand Rapids,42.96,-85.66,Founders Brewing,KBS (Barrel-Aged Stout),All Day IPA (Session IPA)
Michigan,Detroit,42.35,-83.06,Atwater Brewery,Dirty Blonde (Wheat Ale),Vanilla Java Porter (Porter)
Minnesota,Minneapolis,44.97,-93.26,Surly Brewing Co.,Furious (IPA),Axe Man (IPA)
Minnesota,St. Paul,44.95,-93.09,Summit Brewing Co.,Extra Pale Ale (Pale Ale),Sága (IPA)
Minnesota,St. Paul,44.96,-93.10,Barrel Theory Beer,Shooter McGavin (IPA),Rain Drops (Hazy IPA)
Mississippi,Kiln,30.40,-89.43,Lazy Magnolia,Southern Pecan (Nut Brown Ale),Timber Beast (Rye Double IPA)
Mississippi,Hattiesburg,31.32,-89.29,Southern Prohibition,Crowd Control (Double IPA),Suzy B (Blonde Ale)
Mississippi,Gulfport,30.36,-89.09,Chandeleur Island,Free Mason (Golden Ale),Surfside (Wheat Ale)
Missouri,Kansas City,39.09,-94.58,Boulevard Brewing,Tank 7 (Saison),Unfiltered Wheat (Wheat Ale)
Missouri,Maplewood,38.61,-90.32,Side Project Brewing,Derivation (Imperial Stout),Fuzzy (Wild Ale)
Missouri,St. Louis,38.62,-90.19,Perennial Artisan,Abraxas (Imperial Stout),Saison de Lis (Saison)
Montana,Missoula,46.87,-113.99,Big Sky Brewing,Moose Drool (Brown Ale),Trout Montana (Pale Ale)
Montana,Missoula,46.88,-114.00,KettleHouse Brewing,Cold Smoke (Scotch Ale),Bongwater (Hemp Ale)
Montana,Bozeman,45.67,-111.04,MAP Brewing Co.,Midas Crush (IPA),Party (Mexican Lager)
Nebraska,La Vista,41.18,-96.04,Kros Strain Brewing,Fairy Nectar (IPA),Helles Creek (Helles Lager)
Nebraska,Lincoln,40.82,-96.68,Zipline Brewing Co.,Copper Alt (Altbier),Oatmeal Porter (Porter)
Nebraska,Papillion,41.15,-96.04,Nebraska Brewing,Cardinal Pale Ale (Pale Ale),EOS (Hefeweizen)
Nevada,Sparks,39.53,-119.75,Revision Brewing,Revision IPA (IPA),Disco Ninja (Hazy IPA)
Nevada,Sparks,39.54,-119.76,Great Basin Brewing,Ichthyosaur ICKY (IPA),Leave No Trace (Lager)
Nevada,Las Vegas,36.16,-115.13,Tenaya Creek Brewery,Bonanza Brown (Brown Ale),Craft Pilsner (Pilsner)
New Hampshire,Hampton,42.94,-70.83,Smuttynose Brewing,Finestkind (IPA),Old Brown Dog (Brown Ale)
New Hampshire,Newington,43.10,-70.83,Stoneface Brewing,Stoneface IPA (IPA),Full Clip (Hazy IPA)
New Hampshire,Dover,43.19,-70.87,Garrison City,Simcoe (IPA),Hazy (Pale Ale)
New Jersey,Ocean,40.24,-74.03,Kane Brewing Co.,Head High (IPA),Overhead (Double IPA)
New Jersey,Atlantic Highlands,40.41,-74.03,Carton Brewing,Boat Beer (Session Ale),077XX (Double IPA)
New Jersey,Fairfield,40.87,-74.29,Magnify Brewing,Vine Shine (IPA),Search (Hazy IPA)
New Mexico,Albuquerque,35.08,-106.65,La Cumbre Brewing,Elevated (IPA),A Slice of Hefen (Hefeweizen)
New Mexico,Albuquerque,35.09,-106.66,Marble Brewery,Double White (Witbier),Desert Fog (Hazy IPA)
New Mexico,Albuquerque,35.10,-106.67,Bosque Brewing,Elephants on Parade (Fruit Beer),IPA (IPA)
New York,Brooklyn,40.67,-73.99,Other Half Brewing,Green City (Hazy IPA),Broccoli (Double IPA)
New York,Lakewood,42.10,-79.32,Southern Tier,Pumking (Imperial Ale),2XIPA (Double IPA)
New York,Cooperstown,42.69,-74.92,Brewery Ommegang,Hennepin (Farmhouse Ale),Three Philosophers (Quadrupel)
North Carolina,Asheville,35.59,-82.55,Wicked Weed,Pernicious (IPA),Freak of Nature (Double IPA)
North Carolina,Morganton,35.74,-81.68,Fonta Flora Brewery,Nebulo Macchia (IPA),Irish Table (Stout)
North Carolina,Asheville,35.58,-82.56,Burial Beer Co.,Surf Wax (IPA),Skillet Donut (Stout)
North Dakota,Fargo,46.87,-96.78,Drekker Brewing,Brain Squeeze (Smoothie Sour),Ectogasm (Hazy IPA)
North Dakota,Fargo,46.88,-96.79,Fargo Brewing Co.,Wood Chipper (IPA),Iron Horse (Pale Ale)
North Dakota,Bismarck,46.80,-100.78,Laughing Sun,Sinister (Belgian Golden),Space Ranger (IPA)
Ohio,Cleveland,41.48,-81.70,Great Lakes Brewing,Dortmunder Gold (Lager),Edmund Fitzgerald (Porter)
Ohio,Columbus,39.96,-83.01,Hoof Hearted Brewing,Musk of the Minotaur (IPA),Roller Blabe (Double IPA)
Ohio,Cincinnati,39.11,-84.51,Rhinegeist Brewery,Truth (IPA),Knowledge (Double IPA)
Oklahoma,Krebs,34.92,-95.71,Prairie Artisan Ales,Bomb! (Imperial Stout),Vape Tricks (Sour)
Oklahoma,Tulsa,36.15,-95.99,American Solera,Terpy (Double IPA),Sherman (IPA)
Oklahoma,Oklahoma City,35.46,-97.51,COOP Ale Works,F5 (IPA),DNR (Belgian Dark Ale)
Oregon,Bend,44.05,-121.31,Deschutes Brewery,Black Butte (Porter),Fresh Squeezed (IPA)
Oregon,Portland,45.52,-122.68,Rogue Ales,Dead Guy (Maibock),Batsquatch (Hazy IPA)
Oregon,Hood River,45.70,-121.52,pFriem Family Brewers,Pilsner (Pilsner),IPA (IPA)
Pennsylvania,Hershey,40.28,-76.65,Tröegs Independent,Nugget Nectar (Imperial Amber),Perpetual (IPA)
Pennsylvania,Downingtown,40.00,-75.70,Victory Brewing,Golden Monkey (Tripel),Prima Pils (Pilsner)
Pennsylvania,Ardmore,40.01,-75.29,Tired Hands Brewing,Alien Church (IPA),Milkshake IPA (IPA)
Rhode Island,Exeter,41.58,-71.55,Tilted Barn Brewery,Chosen One (Double IPA),Cactus (Double IPA)
Rhode Island,Warwick,41.70,-71.41,Proclamation Ale,Tendril (IPA),Derivative (Pale Ale)
Rhode Island,Westerly,41.37,-71.83,Grey Sail Brewing,Captain's Daughter (Double IPA),Flying Jenny (Extra Pale)
South Carolina,Mt. Pleasant,32.83,-79.88,Westbrook Brewing,Gose (Gose),Mexican Cake (Imperial Stout)
South Carolina,Charleston,32.77,-79.93,Charles Towne,Fermentory (Hazy IPA),Sungazer (IPA)
South Carolina,North Charleston,32.85,-79.97,Coast Brewing,HopArt (IPA),Boy King (Double IPA)
South Dakota,Spearfish,44.49,-103.85,Crow Peak Brewing,Canyon Cream Ale (Cream Ale),11th Hour (IPA)
South Dakota,Sioux Falls,43.54,-96.73,Fernson Brewing,Lion's Paw (Lager),Shy Giant (IPA)
South Dakota,Rapid City,44.08,-103.23,Lost Cabin Beer,Dakota Pale (Pale Ale),SoDank (IPA)
Tennessee,Nashville,36.16,-86.78,Bearded Iris Brewing,Homestyle (IPA),Attention Please (Double IPA)
Tennessee,Nashville,36.15,-86.79,Yazoo Brewing Co.,Gerst (Amber Ale),Dos Perros (Brown Ale)
Tennessee,Nashville,36.17,-86.77,Southern Grist,Teal (Hazy IPA),Melted (Sour)
Texas,Austin,30.61,-97.82,Jester King Brewery,Black Metal (Farmhouse Stout),Le Petit Prince (Table Beer)
Texas,Houston,29.77,-95.34,Saint Arnold Brewing,Art Car (IPA),Fancy Lawnmower (Kolsch)
Texas,Dallas,32.79,-96.81,Deep Ellum Brewing,Dallas Blonde (Blonde Ale),Deep Ellum IPA (IPA)
Utah,Salt Lake City,40.76,-111.89,Epic Brewing Co.,Big Bad Baptist (Imperial Stout),Brainless (Belgian Ale)
Utah,Salt Lake City,40.75,-111.90,Uinta Brewing Co.,Hop Nosh (IPA),Cutthroat (Pale Ale)
Utah,Salt Lake City,40.74,-111.91,Squatters Craft,Hop Rising (Double IPA),Juicy IPA (Hazy IPA)
Vermont,Stowe,44.47,-72.68,The Alchemist,Heady Topper (Double IPA),Focal Banger (IPA)
Vermont,Greensboro,44.58,-72.29,Hill Farmstead,Edward (Pale Ale),Abner (Double IPA)
Vermont,Waitsfield,44.18,-72.82,Lawson's Finest,Sip of Sunshine (IPA),Little Sip (IPA)
Virginia,Richmond,37.54,-77.43,The Veil Brewing,Master Shredder (IPA),Dirt Nap (Double IPA)
Virginia,Alexandria,38.80,-77.04,Aslin Beer Co.,Mind the Hop (Double IPA),Orange Starfish (IPA)
Virginia,Richmond,37.55,-77.44,Hardywood Park,Gingerbread Stout (Stout),Richmond Lager (Lager)
Washington,Seattle,47.65,-122.35,Fremont Brewing,Lush (IPA),The Rusty Nail (Stout)
Washington,Seattle,47.61,-122.31,Elysian Brewing,Space Dust (IPA),Men's Room (Red Ale)
Washington,Seattle,47.55,-122.32,Georgetown Brewing,Manny's (Pale Ale),Bodhi (Double IPA)
West Virginia,Cool Ridge,37.64,-81.18,Weathered Ground,Haggard (IPA),Stop & Smell the Citrus (IPA)
West Virginia,Lewisburg,37.80,-80.44,Greenbrier Valley,Devil Anse (IPA),Mothman (Black IPA)
West Virginia,Davis,39.12,-79.46,Stumptown Ales,Holy Citra (Double IPA),Bewildered Blonde (Blonde Ale)
Wisconsin,New Glarus,42.81,-89.63,New Glarus Brewing,Spotted Cow (Farmhouse Ale),Moon Man (Pale Ale)
Wisconsin,Stevens Point,44.52,-89.57,Central Waters,Mudpuppy (Porter),Brewer's Reserve (Stout)
Wisconsin,Milwaukee,43.05,-87.90,Lakefront Brewery,Riverwest Stein (Amber Lager),IPA (India Pale Ale)
Wyoming,Alpine,43.16,-111.02,Melvin Brewing,2x4 (Double IPA),Hubert (Pale Ale)
Wyoming,Jackson,43.47,-110.76,Snake River Brewing,Zonker (Stout),Pako's (IPA)
Wyoming,Sheridan,44.79,-106.95,Black Tooth Brewing,Saddle Bronc (Brown Ale),Bomber Mountain (Amber Ale)"""

# 3. Reading the text CSV into Pandas DataFrame
df = pd.read_csv(io.StringIO(csv_data))

# 4. Creating Hover Text for the Map (Now in English)
df['Hover_Text'] = (
    "<b>" + df['Brewery'] + "</b> (" + df['City'] + ", " + df['State'] + ")<br><br>" +
    "🍺 1. " + df['Beer1'] + "<br>" +
    "🍺 2. " + df['Beer2']
)

# 5. Map Visualization settings
fig = px.scatter_map(
    df, 
    lat="Lat", 
    lon="Lon", 
    hover_name="Brewery",
    hover_data={"Lat": False, "Lon": False, "Hover_Text": True, "State": False, "City": False, "Beer1": False, "Beer2": False},
    color_discrete_sequence=["#FFD700"], # Gold color for markers
    zoom=3.5, 
    height=750
)

# Styling markers and hover template
fig.update_traces(
    marker=dict(size=10, opacity=0.8, symbol='circle'),
    hovertemplate="%{hovertext}"
)

# Dark mode map style
fig.update_layout(map_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})

# 6. Output to screen
st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Detailed Brewery Database")
# Displaying the DataFrame as a sortable/searchable table
st.dataframe(
    df[['State', 'City', 'Brewery', 'Beer1', 'Beer2']].sort_values(by=['State', 'City']), 
    use_container_width=True,
    hide_index=True
)