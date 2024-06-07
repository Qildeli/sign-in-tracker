import {Box, Container, Typography} from "@mui/material";

interface DashboardProps {
    title: string
    children: any
}

function Dashboard({ children, title }: DashboardProps){
    return (
        <Box sx={{ mt: 16 }}>
            <Container maxWidth="xs">
                <Typography variant="h4" gutterBottom align="center" >
                    { title }
              </Typography >
                <Box>{ children }</Box>
            </Container>
        </Box>
    )
}

export default Dashboard
