import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { environment } from '../environment';

const httpLink = createHttpLink({
  uri: `${environment.apiUrl}/graphql`
});

const authLink = setContext(() => {
  const token = localStorage.getItem('token');
  return {
    headers: {
      authorization: token ? `Bearer ${token}` : '',
    },
  };
});

export const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});
