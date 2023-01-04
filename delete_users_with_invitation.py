### DEVELOPED BY PAGERDUTY PROFESSIONAL SERVICES/SUCCESS ON DEMAND
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
### IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
### FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
### AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
### LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
### OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
### THE SOFTWARE.

# Get users from Account.
# Filter all the ones that have the Resend Notification in status True
# Delete those users.

from pdpyras import APISession

API_ACCESS_KEY ='YOUR FULL ACCESS API KEY HERE'
session = APISession(API_ACCESS_KEY)

list_users_aux = []

offset = 0
deleted = 0
# Get all users from Account
response = session.get("/users?limit=100&total=true&offset=" + str(offset))
list_users = response.json()["users"]
# Iterates if there are more than 100 users
while response.json()["more"]:
    limit = response.json()["limit"]
    offset = offset + int(limit)
    response = session.get("/users?limit=100&total=true&offset=" + str(offset))
    list_users_while = response.json()["users"]
    list_users_aux = list_users_aux + list_users_while

final_list = list_users + list_users_aux

print('Total Users in Account: ', len(final_list))

# Iterates the full user list from the account
for items in final_list:
    # Filter only those users which Invitation is in status True
    if items['invitation_sent'] is True:
        print("I'm deleting user " + items['summary'] + " with id: "+ items['id'] )
        # Delete user
        response = session.delete("/users/"+items['id'])
        print(items['id'] + " " + str(response.ok) + response.text)
        deleted = deleted + 1

print('Deleted users: ' + str(deleted))
print('Total Users after process: ' + str(len(final_list)-deleted))

