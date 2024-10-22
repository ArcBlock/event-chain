import React from 'react';
import {MuiThemeProvider} from '@material-ui/core/styles';
import {createGlobalStyle, ThemeProvider} from 'styled-components';
import CssBaseline from '@material-ui/core/CssBaseline';
import {BrowserRouter as Router, Route, Switch, withRouter} from 'react-router-dom';

import ProfilePage from './pages/profile';
import EventsPage from './pages/events';
import EventDetailPage from './pages/event_detail'

import getPageContext from './libs/context';

const GlobalStyle = createGlobalStyle`
  a {
    color: ${props => props.theme.colors.green};
    text-decoration: none;
  }

  pre,code {
    font-family: Consolas, Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono, Bitstream Vera Sans Mono,
      Courier New, monospace, serif;
  }

  pre {
    margin-bottom: 10px;
    border-radius: 10px;
    line-height: 1.5rem;
    padding: 25px;
    color: #ffffff;
    background-color: #222222;
  }
`;

const pageContext = getPageContext();

export const App = () => (
    <MuiThemeProvider theme={pageContext.theme}>
        <ThemeProvider theme={pageContext.theme}>
            <React.Fragment>
                <CssBaseline/>
                <GlobalStyle/>
                <div className="wrapper">
                    <Switch>
                        <Route exact path="/" component={EventsPage}/>
                        <Route exact path="/profile" component={ProfilePage}/>
                        <Route exact path="/events" component={EventsPage}/>
                        <Route path="/detail" component={EventDetailPage}/>
                    </Switch>
                </div>
            </React.Fragment>
        </ThemeProvider>
    </MuiThemeProvider>
);

const WrappedApp = withRouter(App);

export default () => (
    <Router>
        <WrappedApp/>
    </Router>
);
